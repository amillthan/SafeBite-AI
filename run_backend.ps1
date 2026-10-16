
$ErrorActionPreference = "Stop"

$modelPath = "models/safebite_binary_model.joblib"

if (-not (Test-Path $modelPath)) {
    Write-Host "ERROR: Trained SafeBite AI model not found."
    Write-Host "Expected location: $modelPath"
    Write-Host "Restore the trained model before starting the backend."
    exit 1
}

Write-Host "SafeBite AI trained model found."
Write-Host "Starting FastAPI backend..."

python -m uvicorn backend.app.main:app --host 127.0.0.1 --port 8000

if ($LASTEXITCODE -ne 0) {
    exit $LASTEXITCODE
}