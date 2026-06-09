import os

js_path = r"C:\Users\viper\Desktop\SimsMerged\frontend\js\engine.js"

with open(js_path, "r", encoding="utf-8") as f:
    content = f.read()

new_func = """
let cryptoBalance = 0;
let lastCryptoTick = Date.now();

function drawCryptoSprites() {
    let mintRate = 0;
    
    districts.forEach(d => {
        if (d.type === 'BANK') {
            let baseMint = parseFloat(d.settings?.sprite_mint || 500);
            let gas = parseFloat(d.settings?.gas_fee || 0.01);
            let burn = parseFloat(d.settings?.burn_rate || 1.5) / 100.0;
            
            let netYield = baseMint - (baseMint * gas) - (baseMint * burn);
            mintRate += netYield;

            const { isoX, isoY } = toIso(d.x, d.y);
            const time = Date.now() / 1000;
            const bounce = Math.sin(time * 3) * 10 * zoom;
            
            ctx.save();
            ctx.translate(isoX, isoY - 40 * zoom - bounce);
            
            ctx.shadowBlur = 15;
            ctx.shadowColor = '#ffd700';
            ctx.fillStyle = '#ffd700';
            ctx.beginPath();
            ctx.ellipse(0, 0, 10 * zoom, 15 * zoom, 0, 0, Math.PI * 2);
            ctx.fill();
            
            ctx.shadowBlur = 0;
            ctx.strokeStyle = '#cca300';
            ctx.lineWidth = 2 * zoom;
            ctx.beginPath();
            ctx.ellipse(0, 0, 6 * zoom, 10 * zoom, 0, 0, Math.PI * 2);
            ctx.stroke();
            
            ctx.fillStyle = '#fff';
            ctx.font = `bold ${Math.max(10, 10 * zoom)}px Arial`;
            ctx.textAlign = 'center';
            ctx.textBaseline = 'middle';
            ctx.fillText('S', 0, 0);
            
            ctx.restore();
        }
    });
    
    const now = Date.now();
    const dt = (now - lastCryptoTick) / 1000.0;
    lastCryptoTick = now;
    
    if (mintRate > 0) {
        cryptoBalance += mintRate * dt;
        const rateEl = document.getElementById('mint-rate');
        const balEl = document.getElementById('crypto-balance');
        if (rateEl) rateEl.innerText = mintRate.toFixed(2) + ' SPRITE/s';
        if (balEl) balEl.innerText = cryptoBalance.toFixed(2);
    }
}

function draw() {"""

content = content.replace("function draw() {", new_func)

content = content.replace("drawHolograms();", "drawHolograms();\n    drawCryptoSprites();")

with open(js_path, "w", encoding="utf-8") as f:
    f.write(content)

print("Engine patched with Crypto Logistics!")
