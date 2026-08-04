#!/usr/bin/env pwsh

Write-Host "Running isort..." -ForegroundColor Cyan
isort sagittarius_engine tests Binace_Bot examples

Write-Host "Running black..." -ForegroundColor Cyan
black sagittarius_engine tests Binace_Bot examples

Write-Host "Running ruff..." -ForegroundColor Cyan
ruff check sagittarius_engine tests Binace_Bot examples --fix

Write-Host "Running mypy..." -ForegroundColor Cyan
mypy sagittarius_engine tests Binace_Bot examples

Write-Host "Linting complete!" -ForegroundColor Green
