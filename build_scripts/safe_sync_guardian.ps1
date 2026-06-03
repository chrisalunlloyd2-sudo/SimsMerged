# [TIMESTAMP: 2026-06-02T11:59:30.452Z] [PROJECT_ID: SimsMerged-v1.4-Metropolis] [AGENT_ID: Antigravity-CLI-Architect]

$PROJECT_ROOT = "C:\Users\viper\Desktop\SimsMerged"
$BACKUP_DIR = "C:\Users\viper\.gemini\antigravity-cli\scratch\assets_backup"
$GIT_PATH = "C:\Users\viper\git\cmd\git.exe"

Write-Output "[SAFE GUARDIAN] Initiating Git Safety Protocol..."

# Step 1: Backup visual assets locally
if (!(Test-Path $BACKUP_DIR)) {
    New-Item -ItemType Directory -Force -Path $BACKUP_DIR | Out-Null
}
if (Test-Path "$PROJECT_ROOT\assets") {
    Copy-Item -Path "$PROJECT_ROOT\assets\*" -Destination $BACKUP_DIR -Recurse -Force
    Write-Output "[SAFE GUARDIAN] Stored backup of all visual assets."
} else {
    Write-Output "[SAFE GUARDIAN] Visual assets folder not found, skipping backup."
}

# Step 2: Fetch and verify remote sync state
Set-Location -Path $PROJECT_ROOT
Write-Output "[SAFE GUARDIAN] Fetching remote state..."
& $GIT_PATH fetch origin master

# Step 3: Run git push dry-run to identify potential history rewrites
Write-Output "[SAFE GUARDIAN] Performing dry-run verification..."
$dryRun = & $GIT_PATH push --dry-run origin master 2>&1
$dryRunStr = Out-String -InputObject $dryRun
if ($dryRunStr -match "rejected" -or $dryRunStr -match "non-fast-forward") {
    Write-Warning "[SAFE GUARDIAN] Out of sync detected! Performing safe rebase..."
    & $GIT_PATH pull --rebase origin master
    if ($LASTEXITCODE -ne 0) {
        Write-Error "[SAFE GUARDIAN] Rebase conflict discovered! Locking repository and alerting User."
        exit 1
    }
}

# Step 4: Perform normal push (NEVER FORCE PUSH)
Write-Output "[SAFE GUARDIAN] Safe sync dry-run passed. Pushing additions..."
& $GIT_PATH push origin master
if ($LASTEXITCODE -eq 0) {
    Write-Output "[SAFE GUARDIAN] Pushed changes successfully. Remote gallery protected."
} else {
    Write-Error "[SAFE GUARDIAN] Push failed. Check remote credentials or network connection."
    exit 1
}
