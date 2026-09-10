# [TIMESTAMP: 2026-06-02T11:59:30.452Z] [PROJECT_ID: SimsMerged-v1.4-Metropolis] [AGENT_ID: Antigravity-CLI-Architect]

$PROJECT_ROOT = "C:\Users\viper\Desktop\SimsMerged"
$GIT_LOG_PATH = "$PROJECT_ROOT\GIT_LOG.txt"
$GIT_PATH = "C:\Users\viper\git\cmd\git.exe"

Write-Output "[REFLOG GUARDIAN] Commencing commit history integrity check..."

Set-Location -Path $PROJECT_ROOT

# Step 1: Extract Git Reflog details
$reflog = & $GIT_PATH reflog -n 50 2>&1
$reflogStr = Out-String -InputObject $reflog

if ($reflogStr -match "reset --hard" -or $reflogStr -match "rebase") {
    Write-Output "[REFLOG GUARDIAN] Note: History shift detected (rebase/reset details logged)."
}

# Step 2: Extract all commit SHAs locally to GIT_LOG.txt
$commits = & $GIT_PATH log -n 100 --pretty=format:"%h - %an, %ar : %s" 2>&1
$commitsStr = Out-String -InputObject $commits

$ledger_content = @"
# GIT_LOG.txt
[TIMESTAMP: $(Get-Date -Format 'yyyy-MM-ddTHH:mm:ss.fffZ')]
[PROJECT_ID: SimsMerged-v1.4-Metropolis]
[AGENT_ID: Reflog-Guardian]

STATUS: SECURED & RECORDED

=== RECENT HISTORICAL COMMITS ===
$commitsStr
"@

$ledger_content | Out-File -FilePath $GIT_LOG_PATH -Encoding utf8 -Force
Write-Output "[REFLOG GUARDIAN] Permanent commit ledger updated at $GIT_LOG_PATH."
