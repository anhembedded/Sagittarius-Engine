#!/usr/bin/env pwsh

Write-Host "========================================" -ForegroundColor Blue
Write-Host "      Running Local CI Checks           " -ForegroundColor Blue
Write-Host "========================================" -ForegroundColor Blue

Write-Host "`n[1/5] Ruff — lint" -ForegroundColor Cyan
ruff check sagittarius_engine tests
if ($LASTEXITCODE -ne 0) { Write-Host "Ruff lint failed!" -ForegroundColor Red; exit $LASTEXITCODE }

Write-Host "`n[2/5] Ruff — format check" -ForegroundColor Cyan
ruff format --check sagittarius_engine tests
if ($LASTEXITCODE -ne 0) { Write-Host "Ruff format check failed!" -ForegroundColor Red; exit $LASTEXITCODE }

Write-Host "`n[3/5] mypy — type check" -ForegroundColor Cyan
mypy sagittarius_engine tests --ignore-missing-imports --follow-imports=skip
if ($LASTEXITCODE -ne 0) { Write-Host "mypy type check failed!" -ForegroundColor Red; exit $LASTEXITCODE }

Write-Host "`n[4/5] Run tests with coverage" -ForegroundColor Cyan
pytest tests/ --ignore=tests/benchmark_runtime.py --cov=sagittarius_engine --cov-report=xml --cov-report=term-missing --cov-fail-under=80 -q
if ($LASTEXITCODE -ne 0) { Write-Host "Unit tests failed!" -ForegroundColor Red; exit $LASTEXITCODE }

Write-Host "`n[5/5] Run architecture tests" -ForegroundColor Cyan
pytest tests/test_architecture.py -v
if ($LASTEXITCODE -ne 0) { Write-Host "Architecture tests failed!" -ForegroundColor Red; exit $LASTEXITCODE }

Write-Host "`n========================================" -ForegroundColor Green
Write-Host " All local checks passed successfully!  " -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Green
