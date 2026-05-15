Add-Type -AssemblyName System.Windows.Forms
Add-Type -AssemblyName System.Drawing

$repoPath = "C:\Users\viper\Desktop\Final_Boss_Automation"

# Open the frontend dashboard
Start-Process "$repoPath\frontend\index.html"

# Wait a brief moment for the browser to launch
Start-Sleep -Seconds 2

# Take a screenshot of the active environment
$screenshotPath = "$repoPath\Final_Boss_Environment_Screenshot.png"
$screen = [System.Windows.Forms.Screen]::PrimaryScreen.Bounds
$bitmap = New-Object System.Drawing.Bitmap $screen.Width, $screen.Height
$graphics = [System.Drawing.Graphics]::FromImage($bitmap)
$graphics.CopyFromScreen($screen.Location, [System.Drawing.Point]::Empty, $screen.Size)
$bitmap.Save($screenshotPath, [System.Drawing.Imaging.ImageFormat]::Png)

$graphics.Dispose()
$bitmap.Dispose()

Write-Host "Screenshot captured successfully at: $screenshotPath"
