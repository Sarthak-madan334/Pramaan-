"""Run local resume-to-JSON inference with the saved Pramaan LoRA adapter."""

from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path

from ml.train.prepare_dataset import SYSTEM_PROMPT
from ml.train.train_sft import MODEL_ID


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    source = parser.add_mutually_exclusive_group(required=True)
    source.add_argument("--text", help="Resume text to process (use a file to avoid shell history).")
    source.add_argument("--input-file", type=Path, help="UTF-8 text file containing a resume.")
    parser.add_argument(
        "--adapter",
        type=Path,
        default=Path("ml/checkpoints/pramaan-extractor-xpu-100step/adapter"),
    )
    parser.add_argument("--model", default=MODEL_ID)
    parser.add_argument("--device", choices=("auto", "xpu", "cuda"), default="auto")
    parser.add_argument("--max-input-tokens", type=int, default=512)
    parser.add_argument("--max-new-tokens", type=int, default=512)
    args = parser.parse_args()

    if args.input_file:
        resume_text = args.input_file.read_text(encoding="utf-8").strip()
    else:
        resume_text = args.text.strip()
    if not resume_text:
        raise SystemExit("Resume text is empty.")
    if not args.adapter.is_dir():
        raise SystemExit(f"Adapter directory not found: {args.adapter}")

    private_root = Path("ml/data/private").resolve()
    os.environ["HF_HOME"] = str(private_root / "hf-home")

    import torch
    from peft import PeftModel
    from transformers import AutoModelForCausalLM, AutoTokenizer

    device = args.device
    available = {
        "xpu": hasattr(torch, "xpu") and torch.xpu.is_available(),
        "cuda": torch.cuda.is_available(),
    }
    if device == "auto":
        device = "xpu" if available["xpu"] else "cuda" if available["cuda"] else ""
    if not device or not available[device]:
        raise SystemExit("No supported accelerator is available; inference requires XPU or CUDA.")

    bf16_supported = (
        torch.xpu.is_bf16_supported() if device == "xpu" else torch.cuda.is_bf16_supported()
    )
    compute_dtype = torch.bfloat16 if bf16_supported else torch.float16
    tokenizer = AutoTokenizer.from_pretrained(args.model)
    model = AutoModelForCausalLM.from_pretrained(
        args.model,
        dtype=compute_dtype,
        low_cpu_mem_usage=True,
    )
    model = PeftModel.from_pretrained(model, args.adapter, is_trainable=False)
    model.to(device)
    model.eval()

    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": "Resume:\n" + resume_text},
    ]
    encoded = tokenizer.apply_chat_template(
        messages,
        add_generation_prompt=True,
        tokenize=True,
        return_tensors="pt",
        truncation=True,
        max_length=args.max_input_tokens,
    )
    input_ids = encoded["input_ids"].to(device)
    with torch.inference_mode():
        output = model.generate(
            input_ids,
            max_new_tokens=args.max_new_tokens,
            do_sample=False,
            pad_token_id=tokenizer.eos_token_id,
        )
    generated = tokenizer.decode(
        output[0, input_ids.shape[-1] :], skip_special_tokens=True
    ).strip()

    start = generated.find("{")
    if start >= 0:
        try:
            result, _ = json.JSONDecoder().raw_decode(generated[start:])
        except json.JSONDecodeError:
            result = None
        else:
            print(json.dumps(result, ensure_ascii=False, indent=2))
            return

    print("Model output was not valid JSON:", file=sys.stderr)
    print(generated)
    raise SystemExit(2)


if __name__ == "__main__":
    main()
