param (
    [Parameter(Mandatory=$false)]
    [ValidateSet("debug", "release")]
    [string]$Mode = "debug"
)

Write-Host "🚀 Launching application in [$Mode] mode..." -ForegroundColor Cyan

# Run the application
python main.py --mode $Mode
