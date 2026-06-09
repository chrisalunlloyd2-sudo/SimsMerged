$content = Get-Content -Path 'C:\Users\viper\Desktop\SimsMerged\frontend\index.html' -Raw
$index = $content.IndexOf('</html>')
if ($index -gt 0) {
    $fixed = $content.Substring(0, $index + 7)
    Set-Content -Path 'C:\Users\viper\Desktop\SimsMerged\frontend\index.html' -Value $fixed -Encoding UTF8
    Write-Host "Fixed HTML file!"
}