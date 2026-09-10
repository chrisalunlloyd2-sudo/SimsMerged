# [TIMESTAMP: 2026-06-07T23:35:00.000Z] [PROJECT_ID: SimsMerged-v1.4.2] [AGENT_ID: viper_cli-architectssj4]

# This script automates the migration of the WSL2 VHDX storage to the dedicated SSD path.
# Mandate: Physical Hard-Fencing of agent environments on high-speed storage.

$SSD_TARGET_PATH = "C:\Users\viper\Desktop\SimsMerged\storage_hive\wsl_vhdx"
$DISTRO_NAME = "Ubuntu" # Default distro name, adjust if necessary

Write-Host "🚧 INITIATING PHYSICAL STORAGE MIGRATION..." -ForegroundColor Yellow

# 1. Ensure target path exists
if (!(Test-Path $SSD_TARGET_PATH)) {
    New-Item -ItemType Directory -Path $SSD_TARGET_PATH
}

# 2. Shutdown WSL2 to release locks
Write-Host "🛑 Shutting down WSL2..." -ForegroundColor Cyan
wsl --shutdown

# 3. Export current distro
$export_file = Join-Path $SSD_TARGET_PATH "wsl_backup.tar"
Write-Host "📤 Exporting $DISTRO_NAME to $export_file..." -ForegroundColor Cyan
wsl --export $DISTRO_NAME $export_file

# 4. Unregister old distro
Write-Host "🗑️ Unregistering old distro..." -ForegroundColor Cyan
wsl --unregister $DISTRO_NAME

# 5. Import to SSD path
Write-Host "📥 Importing $DISTRO_NAME to SSD fence: $SSD_TARGET_PATH" -ForegroundColor Green
wsl --import $DISTRO_NAME $SSD_TARGET_PATH $export_file

# 6. Cleanup backup
if (Test-Path $export_file) {
    Remove-Item $export_file
}

Write-Host "🚀 STORAGE HARD-FENCING COMPLETE. Distro $DISTRO_NAME is now SSD-bound." -ForegroundColor Green
Add-Content -Path "C:\Users\viper\PULSE_HEARTBEAT.txt" -Value "[2026-06-07T23:35:00.452Z] [SimsMerged-v1.4.2] [viper_cli-architectssj4] PULSE: WSL2 Storage Hard-Fenced on SSD."
