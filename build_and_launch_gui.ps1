$ErrorActionPreference = "Stop"

# 1. Environment Variables for Java and Maven
$env:JAVA_HOME = "C:\Users\viper\JavaSetup\jdk-17.0.8.1+1"
$env:M2_HOME = "C:\Users\viper\JavaSetup\apache-maven-3.9.4"
$env:PATH = "$env:JAVA_HOME\bin;$env:M2_HOME\bin;$env:PATH"

# 2. Kill existing running instances of the UI
Write-Host "Checking for running instances of Metropolis GUI..."
Get-CimInstance Win32_Process | Where-Object { $_.CommandLine -match "MetropolisGUI.jar" } | ForEach-Object {
    Write-Host "Killing Process ID: $($_.ProcessId)"
    Stop-Process -Id $_.ProcessId -Force
}

# 3. Build the project using Maven
Write-Host "Compiling JavaFX GUI..."
Set-Location "C:\Users\viper\Desktop\SimsMerged\JavaFX_GUI"
mvn clean package

# 4. Move the fat jar to the Desktop
Write-Host "Moving executable to Desktop..."
Copy-Item ".\target\metropolis-gui-1.0.jar" "C:\Users\viper\Desktop\MetropolisGUI.jar" -Force

# 5. Launch the Jar in the background
Write-Host "Launching MetropolisGUI.jar..."
Set-Location "C:\Users\viper\Desktop"
Start-Process -FilePath "java.exe" -ArgumentList "-jar MetropolisGUI.jar" -NoNewWindow
Write-Host "Done!"
