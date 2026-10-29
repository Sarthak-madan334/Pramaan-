"""Download pinned curated splits and write private PII-reduced JSONL files."""

from __future__ import annotations

import argparse
import hashlib
import json
import urllib.request
from pathlib import Path

from ml.train.train_sft import (
    DATASET_ID,
    DATASET_REVISION,
    _pii_values,
    _redact_text,
    _strip_sensitive_fields,
    sanitize_messages,
)


SYSTEM_PROMPT = (
    "Extract structured information from a resume. Use only facts explicitly supported by the resume. "
    "Do not guess, infer, or invent. Use null for unavailable scalar values and empty lists for unavailable collections. "
    "Return exactly one JSON object."
)


def normalized_messages(row: dict) -> list[dict[str, str]]:
    if isinstance(row.get("messages"), list):
        return sanitize_messages(row["messages"])
    resume = row.get("resume_text")
    target = row.get("target_json")
    if not isinstance(resume, str) or not isinstance(target, dict):
        raise ValueError("expected messages or resume_text plus target_json fields")
    pii_values = _pii_values(target)
    resume = _redact_text(resume, pii_values)
    target = _strip_sensitive_fields(target)
    return [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": "Resume:\n" + resume},
        {"role": "assistant", "content": json.dumps(target, ensure_ascii=False, separators=(",", ":"))},
    ]


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def download(revision: str, split: str, destination: Path, force: bool) -> None:
    destination.parent.mkdir(parents=True, exist_ok=True)
    if destination.exists() and not force:
        return
    url = f"https://huggingface.co/datasets/{DATASET_ID}/resolve/{revision}/curated/{split}.jsonl"
    request = urllib.request.Request(url, headers={"User-Agent": "Pramaan-Phase2-DataPrep/0.1"})
    with urllib.request.urlopen(request, timeout=60) as response, destination.open("wb") as output:
        while chunk := response.read(1024 * 1024):
            output.write(chunk)


def process(source: Path, destination: Path, exclude_keys: set[str] | None = None) -> tuple[int, str, set[str], int]:
    count = 0
    seen = set()
    excluded = 0
    exclude_keys = exclude_keys or set()
    destination.parent.mkdir(parents=True, exist_ok=True)
    with source.open("r", encoding="utf-8") as inp, destination.open("w", encoding="utf-8", newline="\n") as out:
        for line_number, line in enumerate(inp, 1):
            row = json.loads(line)
            messages = normalized_messages(row)
            user_text = "\n".join(message["content"] for message in messages if message["role"] == "user")
            key = hashlib.sha256(" ".join(user_text.lower().split()).encode("utf-8")).hexdigest()
            if key in exclude_keys:
                excluded += 1
                continue
            if key in seen:
                continue
            seen.add(key)
            out.write(json.dumps({"messages": messages}, ensure_ascii=False, separators=(",", ":")) + "\n")
            count += 1
    return count, sha256(destination), seen, excluded


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--revision", default=DATASET_REVISION)
    parser.add_argument("--private-dir", type=Path, default=Path("ml/data/private"))
    parser.add_argument("--force-download", action="store_true")
    args = parser.parse_args()
    private_dir = args.private_dir.resolve()
    raw_dir = private_dir / "downloads" / args.revision
    processed_dir = private_dir / "processed"
    results = {}
    for split in ("train", "validation"):
        source = raw_dir / f"{split}.jsonl"
        download(args.revision, split, source, args.force_download)

    train_count, train_digest, train_keys, _ = process(
        raw_dir / "train.jsonl", processed_dir / "train.jsonl"
    )
    validation_count, validation_digest, _, overlap_removed = process(
        raw_dir / "validation.jsonl",
        processed_dir / "validation.jsonl",
        exclude_keys=train_keys,
    )
    results["train"] = {"records": train_count, "sha256": train_digest}
    results["validation"] = {"records": validation_count, "sha256": validation_digest}

    manifest = {
        "dataset_id": DATASET_ID,
        "dataset_revision": args.revision,
        "model_task": "resume_to_structured_json_extraction",
        "splits": results,
        "test_split_downloaded": False,
        "pii_handling": "remove sensitive target fields; exact-match, email, phone, and URL redaction in message text",
        "deduplication": "exact normalized user-text hash within each split",
        "train_validation_duplicates_removed_from_validation": overlap_removed,
        "train_validation_exact_text_overlap": 0,
        "manual_pii_audit_required": True,
    }
    processed_dir.mkdir(parents=True, exist_ok=True)
    (processed_dir / "manifest.json").write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(manifest, indent=2))


if __name__ == "__main__":
    main()
