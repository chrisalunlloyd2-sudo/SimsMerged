$html_path = "C:\Users\viper\Desktop\SimsMerged\frontend\index.html"
$content = Get-Content -Path $html_path -Raw

# We need to add a total balance to the HUD
$hud_old = "CRYPTO_MINT_RATE: <span id=`"mint-rate`">0.0001 cycles/s</span>"
$hud_new = "CRYPTO_MINT_RATE: <span id=`"mint-rate`">0.0000 SPRITE/s</span><br>`n                SPRITE_BALANCE: <span id=`"crypto-balance`" style=`"color:#ffd700; font-weight:bold;`">0.0000</span>"

$content = $content.Replace($hud_old, $hud_new)
Set-Content -Path $html_path -Value $content -Encoding UTF8
Write-Host "HTML HUD patched for Crypto Logistics!"
