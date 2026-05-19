Write-Host 'INITIALIZING THE ULTIMATE METROPOLIS ENGINE: BLOCK 4 - SYNERGY & TELEMETRY' -ForegroundColor Cyan

# 1. Dependency Checks
Write-Host '--- Phase 1: Dependency Validation ---' -ForegroundColor Yellow
$javaOk = (Get-Command java -ErrorAction SilentlyContinue) -ne $null
$pythonOk = (Get-Command python -ErrorAction SilentlyContinue) -ne $null
$mvnOk = (Get-Command mvn -ErrorAction SilentlyContinue) -ne $null

if (-not $javaOk) { Write-Host '[!] Java not found. Please install JDK 17+.' -ForegroundColor Red }
if (-not $pythonOk) { Write-Host '[!] Python not found. Please install Python 3.9+.' -ForegroundColor Red }
if (-not $mvnOk) { Write-Host '[!] Maven not found. Please install Maven.' -ForegroundColor Red }

if (-not ($javaOk -and $pythonOk)) {
    Write-Host 'CRITICAL DEPENDENCIES MISSING. ABORTING LAUNCH.' -ForegroundColor Red
    # We don't exit here so the user can see the message in some environments, 
    # but we skip the launch.
} else {
    Write-Host '[+] All dependencies verified.' -ForegroundColor Green

    # 2. Sequence Simulation
    Write-Host '--- Phase 2: Quantum Harmonization ---' -ForegroundColor Yellow
    0..10 | ForEach-Object {
        Write-Host "Syncing System Matrix: $(($_ * 10))%..." -ForegroundColor Green
        Start-Sleep -Milliseconds 100
    }

    # 3. Launching Backend
    Write-Host '--- Phase 3: Deploying Metropolis Authority ---' -ForegroundColor Yellow
    Start-Process powershell -ArgumentList "-NoExit", "-Command", "python backend/main.py" -WindowStyle Normal

    # 4. Launching Java Engine
    Write-Host '--- Phase 4: Igniting Java Neo Engine ---' -ForegroundColor Yellow
    if (Test-Path "pom.xml") {
        Start-Process powershell -ArgumentList "-NoExit", "-Command", "mvn javafx:run" -WindowStyle Normal
    } else {
        Write-Host '[!] pom.xml not found. Skipping Java launch.' -ForegroundColor Gray
    }

    Write-Host '--- DEPLOYMENT COMPLETE ---' -ForegroundColor Magenta
    Write-Host 'Access the grid at: http://localhost:8000/api/agents' -ForegroundColor White
    Write-Host 'Open frontend/index.html in your browser to experience the magic!' -ForegroundColor White
}
