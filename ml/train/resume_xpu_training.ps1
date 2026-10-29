$ErrorActionPreference = 'Stop'
$repoRoot = (Resolve-Path (Join-Path $PSScriptRoot '..\..')).Path
Set-Location -LiteralPath $repoRoot
$host.UI.RawUI.WindowTitle = 'Pramaan XPU Training'

$python = Join-Path $repoRoot '.venv-ml\Scripts\python.exe'
& $python -u -m ml.train.train_sft `
    --device xpu `
    --max-steps -1 `
    --output ml/checkpoints/pramaan-extractor-xpu-100step `
    --resume-from-checkpoint ml/checkpoints/pramaan-extractor-xpu-100step/checkpoint-100

if ($LASTEXITCODE -ne 0) {
    Write-Host "Training exited with code $LASTEXITCODE" -ForegroundColor Red
} else {
    Write-Host 'Training finished.' -ForegroundColor Green
}
