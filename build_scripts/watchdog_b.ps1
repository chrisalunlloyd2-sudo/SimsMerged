# [TIMESTAMP: 2026-06-05T01:11:00.000Z] [PROJECT_ID: SimsMerged-v1.4] [AGENT_ID: Antigravity-CLI-Architect]

$ProjectRoot = Resolve-Path "$PSScriptRoot\.."
$PythonWatchdog = "$ProjectRoot\backend\core\watchdog_a.py"
$PythonExe = "C:\Users\viper\python\python.exe"

Write-Host "[WATCHDOG_B] Starting persistence monitor..." -ForegroundColor Cyan

while ($true) {
    # 1. Check Watchdog A (Python)
    $watchdogA = Get-Process | Where-Object {$_.CommandLine -like "*watchdog_a.py*"}
    if (-not $watchdogA) {
        Write-Host "[WATCHDOG_B] Watchdog A offline! Restarting..." -ForegroundColor Yellow
        Start-Process powershell -ArgumentList "-NoExit", "-Command", "& '$PythonExe' '$PythonWatchdog'" -WindowStyle Hidden
    }

    # 2. Check Java Engine (Optional, if we want Java persistence too)
    $javaEngine = Get-Process | Where-Object {$_.ProcessName -eq "java"}
    if (-not $javaEngine) {
        # Check if pom.xml exists to restart Maven
        if (Test-Path "$ProjectRoot\pom.xml") {
             Write-Host "[WATCHDOG_B] Java Engine offline! Attempting restart via Maven..." -ForegroundColor Yellow
             # Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$ProjectRoot'; & 'C:\Users\viper\JavaSetup\apache-maven-3.9.4\bin\mvn.cmd' javafx:run" -WindowStyle Hidden
        }
    }

    Start-Sleep -Seconds 45
}
