# Phase 2 training run: resume extraction

This run uses only `md-zain/resume-parser-dataset` at the pinned revision in
`train_sft.py`. It trains structured extraction from resume text. It does not
train Pramaan's evidence-grounded writing tasks.

## Prepare private data

From the repository root, run:

```powershell
python -m ml.train.prepare_dataset
```

This downloads only the source `train` and `validation` JSONL files into the
Git-ignored `ml/data/private/` directory. It does not download the dataset's
held-out `test` split. The pinned files contain `resume_text` and `target_json`;
the preparer converts these to chat examples, removes contact fields from the
target, redacts values found in those fields plus email, phone and URL patterns
from the resume, removes exact duplicate prompts, drops exact train duplicates
from validation, and records the removed count. It prints counts and hashes,
never resume text.

The source may contain PII not recognized by those rules. Review the prepared
data in restricted local storage before training. No raw or processed data may
be committed or pushed.

## Train

This setup supports an Intel GPU through PyTorch XPU, or an NVIDIA GPU through
CUDA. For this 16 GB Intel Arc laptop, use the default Qwen3-0.6B model and
native Windows Python 3.12. The 8B model and CUDA-only 4-bit QLoRA setup are not
appropriate for this machine. The Windows graphics driver and PyTorch XPU build
must expose the GPU before training can start.

Create a virtual environment, then install the XPU-enabled PyTorch wheel and
the remaining dependencies:

```powershell
py -3.12 -m venv .venv-ml
.\.venv-ml\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install torch==2.10.0+xpu torchvision==0.25.0+xpu torchaudio==2.10.0+xpu --index-url https://download.pytorch.org/whl/xpu
pip install -r ml/train/requirements.txt
python -c "import torch; print(torch.xpu.is_available())"
python -m ml.train.train_sft --device xpu --max-steps 100 --max-length 512
```

The 100-step run is a training smoke run, not a release checkpoint. Confirm the
device check prints `True` before starting. After checking loss, structured
output validity, PII behavior and the independent gold set, run a full
experiment and record results. The test split remains untouched.

## Compare the saved adapter

Evaluate the base model and saved LoRA adapter on the prepared validation split
without updating weights:

```powershell
python -m ml.train.evaluate_sft --device xpu
```

This reports aggregate validation loss and token accuracy only. It does not
measure generated JSON quality or replace an independent test set.

## Try a resume locally

Save a resume as a UTF-8 text file, then run:

```powershell
.\.venv-ml\Scripts\python.exe -m ml.train.predict_sft --device xpu --input-file .\resume.txt
```

The script loads the saved adapter, generates one JSON result, and prints it in
the local terminal. It does not upload the input. The trained target omits
contact and personal-information fields, so this model is not trained to return
those values.

The adapter, run manifest, HF cache and data files all stay in Git-ignored paths.
Do not upload them to the Hub unless the underlying source permissions and
model release terms have been checked separately.
