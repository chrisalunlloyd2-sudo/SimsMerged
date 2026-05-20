$js_path = "C:\Users\viper\Desktop\SimsMerged\frontend\js\engine.js"
$content = Get-Content -Path $js_path -Raw

$new_func = @"
function drawTrajectories() {
    const links = window.activeLinks || [
        { from: 'CPU', to: 'RAM', protocol: 'BUS', color: '#00ff00' },
        { from: 'CPU', to: 'GPU', protocol: 'BUS', color: '#ff00ff' },
        { from: 'CPU', to: 'MODEM', protocol: 'TCP/IP', color: '#00ffff' },
        { from: 'CPU', to: 'LLM', protocol: 'BUS', color: '#00ffff' }
    ];

    // Reactive Logic from AI Attributes
    const attnHeads = parseFloat(window.activeResearchAttrs?.heads || 32);
    const bandwidth = parseFloat(window.activeResearchAttrs?.vocab || 128256) / 100000.0;
    const spawnChance = 0.02 * bandwidth;

    links.forEach(l => {
        const from = districts.find(d => d.type === l.from), to = districts.find(d => d.type === l.to);
        if(from && to) {
            const p1 = toIso(from.x, from.y), p2 = toIso(to.x, to.y);
            ctx.setLineDash(l.protocol === 'BUS' ? [] : [10, 5]);
            
            // Visual feedback: Curve height determined by attention heads
            const curveHeight = (100 * zoom) * (attnHeads / 32.0);
            
            ctx.strokeStyle = l.color + "44"; ctx.lineWidth = 2;
            ctx.beginPath(); ctx.moveTo(p1.isoX, p1.isoY); 
            ctx.quadraticCurveTo((p1.isoX+p2.isoX)/2, (p1.isoY+p2.isoY)/2 - curveHeight, p2.isoX, p2.isoY);
            ctx.stroke();
            
            if(Math.random() < spawnChance) spawnPacket(from.x, from.y, to.x, to.y, l.color, l.protocol);
        }
    });
}
"@

# Replace the entire old function block
$pattern = "(?s)function drawTrajectories\(\) \{.*?\}\n\n"
$content = [regex]::Replace($content, $pattern, $new_func + "`n`n")

Set-Content -Path $js_path -Value $content -Encoding UTF8
Write-Host "Neural Bus Patched!"
