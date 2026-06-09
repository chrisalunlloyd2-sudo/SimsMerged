$js_path = "C:\Users\viper\Desktop\SimsMerged\frontend\js\engine.js"
$content = Get-Content -Path $js_path -Raw

$new_logic = @"
    // 5. Darwinistic Environmental Effects
    const entropy = parseFloat(window.activeResearchAttrs?.dropout || 0.2) * 5.0;
    const heat = parseFloat(window.systemHeat || 35.0);
    
    if (heat > 70 || entropy > 2.0) {
        ctx.save();
        ctx.globalAlpha = 0.1;
        ctx.fillStyle = heat > 80 ? '#f00' : '#f0f';
        for(let i=0; i<entropy*2; i++) {
            ctx.fillRect(Math.random()*canvas.width, Math.random()*canvas.height, 100*zoom, 2*zoom);
        }
        ctx.restore();
    }
    
    requestAnimationFrame(draw);
}
"@

$content = $content.Replace("requestAnimationFrame(draw);`n}", $new_logic)
Set-Content -Path $js_path -Value $content -Encoding UTF8
Write-Host "Darwinistic Horizon Patched!"
