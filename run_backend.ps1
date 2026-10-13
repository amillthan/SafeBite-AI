$ErrorActionPreference = "Stop"

if (-not (Test-Path "artifacts/models/food_safety_classifier.joblib")) {
    Write-Host "Model not found. Generating prototype model..."

    python data/scripts/create_synthetic_dataset.py

    if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }

    python ml/train_baseline.py

    if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
}

python -m uvicorn backend.app.main:app --host 127.0.0.1 --port 8000