# [TIMESTAMP: 2026-06-05T01:14:00.000Z] [PROJECT_ID: SimsMerged-v1.4] [AGENT_ID: Antigravity-CLI-Architect]

$WshShell = New-Object -ComObject WScript.Shell
$ShortcutPath = Join-Path $env:APPDATA "Microsoft\Windows\Start Menu\Programs\Startup\SimsMerged.lnk"
$Shortcut = $WshShell.CreateShortcut($ShortcutPath)
$Shortcut.TargetPath = "powershell.exe"
$Shortcut.Arguments = "-ExecutionPolicy Bypass -File C:\Users\viper\Desktop\SimsMerged\startup_metropolis.ps1"
$Shortcut.WorkingDirectory = "C:\Users\viper\Desktop\SimsMerged"
$Shortcut.WindowStyle = 7 
$Shortcut.Save()
Write-Host "Startup shortcut created at $ShortcutPath"
