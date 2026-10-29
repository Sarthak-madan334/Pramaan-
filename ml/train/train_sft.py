"""LoRA SFT for Pramaan resume extraction using one pinned HF dataset.

Raw dataset/cache and model artifacts stay under ignored ml/data/private and
ml/checkpoints paths. Intel XPU and CUDA accelerators are supported; CPU-only
training is refused.
"""

from __future__ import annotations

import argparse
import json
import os
import re
from pathlib import Path
from typing import Any

DATASET_ID = "md-zain/resume-parser-dataset"
DATASET_REVISION = "5b9cbddf29c8acba243cc2ec8ff722ca2f54c915"
MODEL_ID = "Qwen/Qwen3-0.6B"
SENSITIVE_KEYS = {
    "personal_information",
    "contact_information",
    "full_name",
    "first_name",
    "last_name",
    "email",
    "phone",
    "phone_number",
    "phone_numbers",
    "address",
    "city",
    "state_or_region",
    "postal_code",
    "country",
    "linkedin",
    "portfolio",
    "other_links",
    "references",
}
EMAIL_RE = re.compile(r"\b[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}\b", re.I)
URL_RE = re.compile(r"\b(?:https?://|www\.)\S+", re.I)
PHONE_RE = re.compile(
    r"(?<!\w)(?:\+?\d{1,3}[-.\s]?)?(?:\(?\d{3}\)?[-.\s]?)\d{3}[-.\s]?\d{4}(?!\w)"
    r"|(?<!\w)\+?91[-.\s]?[6-9]\d{9}(?!\w)"
)


def _pii_values(value: Any, sensitive: bool = False) -> list[str]:
    found: list[str] = []
    if isinstance(value, dict):
        for key, child in value.items():
            found.extend(_pii_values(child, sensitive or key.casefold() in SENSITIVE_KEYS))
    elif isinstance(value, list):
        for child in value:
            found.extend(_pii_values(child, sensitive))
    elif sensitive and isinstance(value, (str, int, float)) and str(value).strip():
        found.append(str(value).strip())
    return found


def _strip_sensitive_fields(value: Any) -> Any:
    if isinstance(value, dict):
        return {
            key: (None if key.casefold() in SENSITIVE_KEYS else _strip_sensitive_fields(child))
            for key, child in value.items()
        }
    if isinstance(value, list):
        return [_strip_sensitive_fields(child) for child in value]
    return value


def _redact_text(text: str, known_values: list[str]) -> str:
    for item in sorted(set(known_values), key=len, reverse=True):
        if len(item) >= 2:
            text = re.sub(re.escape(item), "[REDACTED]", text, flags=re.I)
    text = EMAIL_RE.sub("[REDACTED_EMAIL]", text)
    text = URL_RE.sub("[REDACTED_URL]", text)
    text = PHONE_RE.sub("[REDACTED_PHONE]", text)
    return text


def sanitize_messages(messages: Any) -> list[dict[str, str]]:
    if not isinstance(messages, list):
        raise ValueError("record has no conversational messages list")
    assistant_targets = [
        item.get("content")
        for item in messages
        if isinstance(item, dict) and item.get("role") == "assistant"
    ]
    if len(assistant_targets) != 1 or not isinstance(assistant_targets[0], str):
        raise ValueError("expected exactly one string assistant target")

    target_raw = assistant_targets[0]
    try:
        target_obj = json.loads(target_raw)
    except json.JSONDecodeError as exc:
        raise ValueError("assistant target is not valid JSON") from exc
    known_pii = _pii_values(target_obj)
    target_clean = json.dumps(_strip_sensitive_fields(target_obj), ensure_ascii=False, separators=(",", ":"))

    result = []
    for item in messages:
        if not isinstance(item, dict) or item.get("role") not in ("system", "user", "assistant"):
            raise ValueError("message has an invalid role or shape")
        content = item.get("content")
        if not isinstance(content, str):
            raise ValueError("message content must be text")
        if item["role"] == "assistant":
            content = target_clean
        content = _redact_text(content, known_pii)
        result.append({"role": item["role"], "content": content})
    return result


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--model", default=MODEL_ID)
    parser.add_argument("--device", choices=("auto", "xpu", "cuda"), default="auto")
    parser.add_argument("--dataset-revision", default=DATASET_REVISION)
    parser.add_argument("--output", type=Path, default=Path("ml/checkpoints/pramaan-extractor-v0.1"))
    parser.add_argument("--max-steps", type=int, default=-1, help="Use -1 for one pass over the train split")
    parser.add_argument(
        "--resume-from-checkpoint",
        type=Path,
        help="Resume optimizer and model state from a Trainer checkpoint",
    )
    parser.add_argument("--max-length", type=int, default=512)
    args = parser.parse_args()

    private_root = Path("ml/data/private").resolve()
    private_root.mkdir(parents=True, exist_ok=True)
    os.environ["HF_HOME"] = str(private_root / "hf-home")
    os.environ["HF_DATASETS_CACHE"] = str(private_root / "datasets-cache")

    import torch
    from datasets import load_dataset
    from peft import LoraConfig
    from transformers import AutoModelForCausalLM

    available = {
        "xpu": hasattr(torch, "xpu") and torch.xpu.is_available(),
        "cuda": torch.cuda.is_available(),
    }
    device = args.device
    if device == "auto":
        device = "xpu" if available["xpu"] else "cuda" if available["cuda"] else ""
    if not device or not available[device]:
        raise SystemExit(
            "No requested accelerator is available. Intel GPUs use PyTorch XPU; "
            "check the Intel graphics driver and `torch.xpu.is_available()`. "
            "No dataset or model was loaded."
        )
    if device == "xpu":
        # TRL's optional Triton loss kernel tries to compile a Windows C++ helper
        # on first use. The chunked PyTorch implementation works without it.
        import transformers.utils

        transformers.utils.is_triton_available = lambda: False
    from trl import SFTConfig, SFTTrainer
    if args.max_steps == 0 or args.max_steps < -1:
        raise SystemExit("--max-steps must be -1 or a positive integer")

    private_root = Path("ml/data/private").resolve()
    processed_dir = private_root / "processed"
    manifest_path = processed_dir / "manifest.json"
    if not manifest_path.is_file():
        raise SystemExit("Prepared data missing. Run python -m ml.train.prepare_dataset first.")
    source_manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    if source_manifest.get("dataset_revision") != args.dataset_revision:
        raise SystemExit("Prepared data revision differs from --dataset-revision; prepare it again.")

    # Load only PII-scrubbed train and validation JSONL. The held-out test split
    # is intentionally never downloaded or loaded by this training program.
    data = load_dataset(
        "json",
        data_files={
            "train": str(processed_dir / "train.jsonl"),
            "validation": str(processed_dir / "validation.jsonl"),
        },
    )
    train = data["train"]
    validation = data["validation"]

    bf16_supported = (
        torch.xpu.is_bf16_supported() if device == "xpu" else torch.cuda.is_bf16_supported()
    )
    compute_dtype = torch.bfloat16 if bf16_supported else torch.float16
    model = AutoModelForCausalLM.from_pretrained(
        args.model,
        dtype=compute_dtype,
        low_cpu_mem_usage=True,
    )
    model.config.use_cache = False
    peft = LoraConfig(
        r=16,
        lora_alpha=32,
        lora_dropout=0.05,
        target_modules="all-linear",
        task_type="CAUSAL_LM",
    )
    args.output.mkdir(parents=True, exist_ok=True)
    trainer = SFTTrainer(
        model=model,
        train_dataset=train,
        eval_dataset=validation,
        peft_config=peft,
        args=SFTConfig(
            output_dir=str(args.output),
            max_length=args.max_length,
            assistant_only_loss=True,
            learning_rate=1e-4,
            num_train_epochs=1,
            max_steps=args.max_steps,
            per_device_train_batch_size=1,
            per_device_eval_batch_size=1,
            gradient_accumulation_steps=4,
            gradient_checkpointing=True,
            bf16=compute_dtype == torch.bfloat16,
            fp16=compute_dtype == torch.float16,
            logging_steps=10,
            eval_strategy="steps",
            eval_steps=100,
            save_strategy="steps",
            save_steps=100,
            save_total_limit=2,
            optim="adamw_torch",
            dataloader_pin_memory=False,
            report_to="none",
            seed=42,
        ),
    )
    trainer.train(
        resume_from_checkpoint=(
            str(args.resume_from_checkpoint) if args.resume_from_checkpoint else None
        )
    )
    trainer.save_model(str(args.output / "adapter"))
    (args.output / "run-manifest.json").write_text(
        json.dumps(
            {
                "dataset": DATASET_ID,
                "dataset_revision": args.dataset_revision,
                "model": args.model,
            "device": device,
            "precision": "bf16" if compute_dtype == torch.bfloat16 else "fp16",
                "train_records": len(train),
                "validation_records": len(validation),
                "test_split_loaded": False,
                "pii_redaction": "email, phone, URL, and fields identified in target JSON",
                "max_length": args.max_length,
                "max_steps": args.max_steps,
                "per_device_train_batch_size": 1,
                "gradient_accumulation_steps": 4,
                "effective_batch_size": 4,
                "seed": 42,
            },
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )
    print(f"Adapter saved to {args.output / 'adapter'}")


if __name__ == "__main__":
    main()
