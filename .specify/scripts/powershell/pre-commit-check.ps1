#!/usr/bin/env pwsh
# Pre-commit validation script
# Runs format, lint, and tests before allowing commit

$ErrorActionPreference = "Stop"

Write-Host "==> Running pre-commit checks..." -ForegroundColor Cyan

# Step 1: Format code
Write-Host "`n==> Step 1/3: Formatting code with ruff..." -ForegroundColor Yellow
uv run ruff format src/ tests/
if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ Formatting failed!" -ForegroundColor Red
    exit 1
}
Write-Host "✓ Formatting passed" -ForegroundColor Green

# Step 2: Lint code
Write-Host "`n==> Step 2/3: Linting code with ruff..." -ForegroundColor Yellow
uv run ruff check src/ tests/
if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ Linting failed!" -ForegroundColor Red
    exit 1
}
Write-Host "✓ Linting passed" -ForegroundColor Green

# Step 3: Run tests
Write-Host "`n==> Step 3/3: Running tests with pytest..." -ForegroundColor Yellow
uv run pytest
if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ Tests failed!" -ForegroundColor Red
    exit 1
}
Write-Host "✓ Tests passed" -ForegroundColor Green

Write-Host "`n✓ All pre-commit checks passed! Ready to commit." -ForegroundColor Green
exit 0
