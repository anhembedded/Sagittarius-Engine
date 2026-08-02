<#
.SYNOPSIS
Runs the Audit Dashboard application.

.DESCRIPTION
This script activates the virtual environment (if available) and runs the Audit Dashboard.
It supports running the full application or just the UI component.

.PARAMETER UiOnly
If specified, runs the dashboard in UI-only mode without connecting to the backend.

.EXAMPLE
.\run_dashboard.ps1
Runs the full application.

.EXAMPLE
.\run_dashboard.ps1 -UiOnly
Runs only the UI.
#>

param (
    [switch]$UiOnly
)

$ErrorActionPreference = "Stop"

# Get the directory where this script is located
$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Definition

# The main repository root is two levels up from tools/audit_dashboard
$RepoRoot = Resolve-Path (Join-Path $ScriptDir "..\..")

# Path to the virtual environment activation script
$VenvActivate = Join-Path $RepoRoot ".venv\Scripts\Activate.ps1"

if (Test-Path $VenvActivate) {
    Write-Host "Activating virtual environment..." -ForegroundColor Cyan
    . $VenvActivate
} else {
    Write-Warning "Virtual environment not found at $VenvActivate. Running with system Python."
}

# Change to the dashboard directory to ensure relative paths work correctly
Set-Location $ScriptDir

# Construct the command
$PythonCmd = "python"
$ScriptArgs = @("main.py")

if ($UiOnly) {
    Write-Host "Starting Audit Dashboard in UI-Only mode..." -ForegroundColor Green
    $ScriptArgs += "--ui-only"
} else {
    Write-Host "Starting full Audit Dashboard..." -ForegroundColor Green
}

# Add the repo root to PYTHONPATH so sagittarius_engine can be imported
$env:PYTHONPATH = $RepoRoot

# Run the python script
& $PythonCmd $ScriptArgs

if ($LASTEXITCODE -ne 0) {
    Write-Error "Application exited with code $LASTEXITCODE"
}
