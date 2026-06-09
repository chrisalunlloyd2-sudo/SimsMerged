@echo off
echo ====================================================
echo [GITHUB AUTOMATION] Initiating Add-Only Sync
echo ====================================================
echo.
echo Executing Viper Script Pyramid Backup Protocol...

:: 1. Run the local sync
call C:\Users\viper\SimAgentCity\git_sync.bat

echo.
echo [STATUS] Local Add-Only mirror synchronized at C:\Users\viper\SimAgentCity_Backup
echo [STATUS] High-Fitness ToK components synced to C:\Users\viper\OneDrive\Desktop\ViperNotes\src
echo.
echo ====================================================
echo [MANUAL PUSH REQUIRED]
echo To push to your remote GitHub repository, open a host terminal and run:
echo cd C:\Users\viper\SimAgentCity_Backup
echo git add .
echo git commit -m "Automated Add-Only Genesis Sync"
echo git push origin main
echo ====================================================
pause
