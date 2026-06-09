import os

js_path = r"C:\Users\viper\Desktop\SimsMerged\frontend\js\engine.js"

with open(js_path, "r", encoding="utf-8") as f:
    content = f.read()

# We want to add environmental effects based on active research attrs
new_draw_loop_extension = """
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
"""

content = content.replace("requestAnimationFrame(draw);\n}", new_draw_loop_extension)

with open(js_path, "w", encoding="utf-8") as f:
    f.write(content)

print("Engine patched: Darwinistic Horizon effects are now live!")
