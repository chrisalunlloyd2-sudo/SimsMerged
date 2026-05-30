Write-Host 'INITIALIZING THE ULTIMATE METROPOLIS ENGINE: BLOCK 4 - SYNERGY & TELEMETRY' -ForegroundColor Cyan

# 1. Path Configuration
$JAVA_HOME = "C:\Users\viper\JavaSetup\jdk-17.0.8.1+1"
$PYTHON_PATH = "C:\Users\viper\python\python.exe"
$MVN_PATH = "C:\Users\viper\JavaSetup\apache-maven-3.9.4\bin\mvn.cmd"

$env:JAVA_HOME = $JAVA_HOME
$env:PATH = "$JAVA_HOME\bin;$env:PATH"

# 2. Dependency Checks
Write-Host '--- Phase 1: Dependency Validation ---' -ForegroundColor Yellow
$javaOk = Test-Path "$JAVA_HOME\bin\java.exe"
$pythonOk = Test-Path $PYTHON_PATH
$mvnOk = Test-Path $MVN_PATH

if (-not $javaOk) { Write-Host "[!] Java not found at $JAVA_HOME" -ForegroundColor Red }
if (-not $pythonOk) { Write-Host "[!] Python not found at $PYTHON_PATH" -ForegroundColor Red }
if (-not $mvnOk) { Write-Host "[!] Maven not found at $MVN_PATH" -ForegroundColor Red }

if (-not ($javaOk -and $pythonOk -and $mvnOk)) {
    Write-Host 'CRITICAL DEPENDENCIES MISSING. ABORTING LAUNCH.' -ForegroundColor Red
} else {
    Write-Host '[+] All dependencies verified.' -ForegroundColor Green

    # 3. Sequence Simulation (Optimized)
    Write-Host '--- Phase 2: Quantum Harmonization ---' -ForegroundColor Yellow
    Write-Host "Syncing System Matrix: 100%..." -ForegroundColor Green


    # 4. Launching Backend
    Write-Host '--- Phase 3: Deploying Metropolis Authority ---' -ForegroundColor Yellow
    # Using the new run_backend.py to ensure project root is in PYTHONPATH
    Start-Process powershell -ArgumentList "-NoExit", "-Command", "& '$PYTHON_PATH' run_backend.py" -WindowStyle Normal

    # 5. Launching Java Engine
    Write-Host '--- Phase 4: Igniting Java Neo Engine ---' -ForegroundColor Yellow
    if (Test-Path "pom.xml") {
        Start-Process powershell -ArgumentList "-NoExit", "-Command", "& '$MVN_PATH' javafx:run" -WindowStyle Normal
    } else {
        Write-Host '[!] pom.xml not found. Skipping Java launch.' -ForegroundColor Gray
    }

    Write-Host '--- DEPLOYMENT COMPLETE ---' -ForegroundColor Magenta
    Write-Host 'Access the grid at: http://localhost:8000/api/agents' -ForegroundColor White
    Write-Host 'Open frontend/index.html in your browser to experience the magic!' -ForegroundColor White
}
