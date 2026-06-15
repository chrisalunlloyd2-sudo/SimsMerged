# [TIMESTAMP: 2026-06-11T03:50:00.000Z] [PROJECT_ID: SimsMerged-v1.4.2] [AGENT_ID: Gemini-CLI-Architect]
# PHASE 29: QWEN CODER & OLLAMA SETUP

$OLLAMA_EXE = "$env:LOCALAPPDATA\Ollama\ollama.exe"
if (-not (Test-Path $OLLAMA_EXE)) {
    Write-Host "⚠️ Ollama not found in $OLLAMA_EXE. Searching..."
    $OLLAMA_EXE = (Get-Command ollama.exe -ErrorAction SilentlyContinue).Source
}

if (-not $OLLAMA_EXE) {
    Write-Host "❌ Ollama is not installed. Please install Ollama first."
    exit 1
}

Write-Host "🌀 Initializing Qwen-Coder Models for Sprite Triplet..."
& $OLLAMA_EXE pull qwen2.5-coder:0.5b
& $OLLAMA_EXE pull qwen2.5-coder:1.5b
& $OLLAMA_EXE pull qwen2.5-coder:7b

Write-Host "✅ Qwen Coder Models Hydrated."

# Registering as a CLI tool in the project
$BIN_DIR = "C:\Users\viper\Desktop\SimsMerged\backend\bin"
if (-not (Test-Path $BIN_DIR)) { New-Item -Path $BIN_DIR -ItemType Directory }

$CLI_WRAPPER = "$BIN_DIR\qwen-coder.ps1"
Set-Content -Path $CLI_WRAPPER -Value @"
# Qwen Coder CLI Wrapper
`$OLLAMA_EXE run qwen2.5-coder:7b `$args
"@

Write-Host "🚀 Qwen Coder CLI wrapper created at $CLI_WRAPPER"
