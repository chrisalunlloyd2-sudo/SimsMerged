# [TIMESTAMP: 2026-06-05T01:12:00.000Z] [PROJECT_ID: SimsMerged-v1.4] [AGENT_ID: Antigravity-CLI-Architect]

$ProjectRoot = $PSScriptRoot
Set-Location $ProjectRoot

Write-Host "INITIALIZING METROPOLIS STARTUP SEQUENCE..." -ForegroundColor Magenta

# 1. Start Environment
Write-Host "Starting environment..." -ForegroundColor Cyan
& '.\start_environment.ps1'

# 2. Start Watchdogs
Write-Host "Launching Double Watchdog Persistence..." -ForegroundColor Green
$PythonExe = "C:\Users\viper\python\python.exe"
$WatchdogA = ".\backend\core\watchdog_a.py"
$WatchdogB = ".\build_scripts\watchdog_b.ps1"

Start-Process powershell -ArgumentList "-NoExit", "-Command", "& '$PythonExe' '$WatchdogA'" -WindowStyle Hidden
Start-Process powershell -ArgumentList "-NoExit", "-Command", "& 'powershell.exe' -File '$WatchdogB'" -WindowStyle Hidden

Write-Host "METROPOLIS IS NOW PERSISTENT." -ForegroundColor White
