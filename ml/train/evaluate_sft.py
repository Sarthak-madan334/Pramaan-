"""Compare the base model and a saved Pramaan LoRA adapter on validation data.

Only aggregate loss and token-accuracy metrics are printed. The prepared
dataset and model cache remain under Git-ignored ml/data/private paths.
"""

from __future__ import annotations

import argparse
import json
import os
from pathlib import Path

from ml.train.train_sft import DATASET_REVISION, MODEL_ID


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--adapter",
        type=Path,
        default=Path("ml/checkpoints/pramaan-extractor-xpu-100step/adapter"),
    )
    parser.add_argument("--model", default=MODEL_ID)
    parser.add_argument("--device", choices=("auto", "xpu", "cuda"), default="auto")
    parser.add_argument("--max-length", type=int, default=512)
    args = parser.parse_args()

    private_root = Path("ml/data/private").resolve()
    os.environ["HF_HOME"] = str(private_root / "hf-home")
    os.environ["HF_DATASETS_CACHE"] = str(private_root / "datasets-cache")
    processed_dir = private_root / "processed"
    source_manifest = json.loads((processed_dir / "manifest.json").read_text(encoding="utf-8"))
    if source_manifest.get("dataset_revision") != DATASET_REVISION:
        raise SystemExit("Prepared data revision differs from the pinned training revision.")
    if not args.adapter.is_dir():
        raise SystemExit(f"Adapter directory not found: {args.adapter}")

    import torch
    from datasets import load_dataset
    from peft import PeftModel
    from transformers import AutoModelForCausalLM

    device = args.device
    available = {
        "xpu": hasattr(torch, "xpu") and torch.xpu.is_available(),
        "cuda": torch.cuda.is_available(),
    }
    if device == "auto":
        device = "xpu" if available["xpu"] else "cuda" if available["cuda"] else ""
    if not device or not available[device]:
        raise SystemExit("No supported accelerator is available; evaluation requires XPU or CUDA.")
    if device == "xpu":
        # Avoid TRL's optional Windows Triton helper; use its PyTorch loss path.
        import transformers.utils

        transformers.utils.is_triton_available = lambda: False
    from trl import SFTConfig, SFTTrainer

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
    eval_config = SFTConfig(
        output_dir=str(private_root / "evaluation-cache"),
        max_length=args.max_length,
        assistant_only_loss=True,
        per_device_eval_batch_size=1,
        gradient_checkpointing=False,
        bf16=compute_dtype == torch.bfloat16,
        fp16=compute_dtype == torch.float16,
        dataloader_pin_memory=False,
        report_to="none",
        seed=42,
    )

    results: dict[str, object] = {
        "dataset_revision": DATASET_REVISION,
        "validation_records": len(validation),
        "model": args.model,
        "adapter": str(args.adapter),
        "device": device,
        "precision": "bf16" if compute_dtype == torch.bfloat16 else "fp16",
        "max_length": args.max_length,
    }

    for label in ("base", "adapter"):
        model = AutoModelForCausalLM.from_pretrained(
            args.model,
            dtype=compute_dtype,
            low_cpu_mem_usage=True,
        )
        model.config.use_cache = False
        if label == "adapter":
            model = PeftModel.from_pretrained(model, args.adapter, is_trainable=False)
        # TRL requires a nonempty train dataset at construction. Pass one
        # training example for setup; evaluate() below never invokes train().
        trainer = SFTTrainer(
            model=model,
            train_dataset=train.select(range(1)),
            eval_dataset=validation,
            args=eval_config,
        )
        metrics = trainer.evaluate()
        results[label] = {
            key: round(float(metrics[key]), 6)
            for key in ("eval_loss", "eval_mean_token_accuracy", "eval_runtime")
            if key in metrics
        }
        del trainer, model
        if device == "xpu":
            torch.xpu.empty_cache()
        elif device == "cuda":
            torch.cuda.empty_cache()

    print(json.dumps(results, indent=2))


if __name__ == "__main__":
    main()
