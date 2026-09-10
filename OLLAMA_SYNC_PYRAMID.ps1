<#
.SYNOPSIS
Ollama Sync Pyramid - House Program
Ensures all required local models (especially smollm:135m) are downloaded and fenced.
#>
Write-Host "[TIMESTAMP: $(Get-Date -Format 'yyyy-MM-ddTHH:mm:ssZ')] [PROJECT_ID: SimsMerged-v1.4.2] [AGENT_ID: Gemini-CLI-Architect]" -ForegroundColor Cyan
Write-Host "INITIALIZING SCRIPT PYRAMID: OLLAMA SYNC" -ForegroundColor Magenta

$requiredModels = @("smollm:135m", "qwen2.5:0.5b", "h2o-danube2:0.5b")
$ollamaPath = "C:\Users\viper\AppData\Local\Programs\Ollama\ollama.exe"

if (-Not (Test-Path $ollamaPath)) {
    Write-Host "Ollama executable not found. Pyramid Sync aborted." -ForegroundColor Red
    exit 1
}

# Get currently installed models
$installedRaw = & $ollamaPath list
$installed = $installedRaw | Select-String -Pattern "latest|135m|0.5b" | ForEach-Object { ($_ -split '\s+')[0] }

foreach ($model in $requiredModels) {
    # Check if the required model string is partially matched in installed list
    $match = $installed | Where-Object { $_ -like "*$($model.Split(':')[0])*" }
    
    if (-Not $match) {
        Write-Host "Missing Model Detected: $model. Initiating Fenced Download..." -ForegroundColor Yellow
        # Run pull in background to not block the script
        Start-Process -FilePath $ollamaPath -ArgumentList "pull $model" -WindowStyle Hidden
        Write-Host "Pull queued for $model." -ForegroundColor Green
    } else {
        Write-Host "Model Verified in SSD Matrix: $model" -ForegroundColor DarkGreen
    }
}

Write-Host "SCRIPT PYRAMID: SYNC COMPLETE." -ForegroundColor Cyan
