// PRESERVE AND PROTECT: Safe GUI Extensions Hook
// Extends chat with missing context-clear and logit chart, and adds the Clippy Control Pad.
// [TIMESTAMP: 2026-06-08T04:10:00.000Z]

(function() {
    // --- 1. SAFELY HOOK MISSING CHAT COMPONENTS ---
    try {
        const chatContainer = document.getElementById('msn-chat-container');
        if (chatContainer) {
            const chatToolbar = document.createElement('div');
            chatToolbar.style.cssText = 'padding: 2px; background: #dfdfdf; display: flex; gap: 2px; border-top: 1px solid #808080;';
            
            const clearBtn = document.createElement('button');
            clearBtn.innerText = 'CLEAR_CONTEXT';
            clearBtn.style.cssText = 'flex: 1; font-size: 8px; padding: 1px; cursor: pointer; background: #000; color: #ff0000; border: 1px solid #ff0000;';
            clearBtn.onclick = function() {
                const log = document.getElementById('msn-log');
                if (log) {
                    log.innerHTML = '<div style="color:#ff0000; font-size:9px;">[SYSTEM: CONTEXT MEMORY PURGED]</div>';
                    // Safe Polyfill Bridge: clear backend context if function exists
                    if (typeof window.triggerMemoryFlush === 'function') window.triggerMemoryFlush();
                }
            };

            const logitBtn = document.createElement('button');
            logitBtn.innerText = 'LOGIT_TRACKER';
            logitBtn.style.cssText = 'flex: 1; font-size: 8px; padding: 1px; cursor: pointer; background: #000; color: #00ffff; border: 1px solid #00ffff;';
            logitBtn.onclick = function() {
                if (window.showNotification) {
                    window.showNotification("LOGIT TRACKER", "Logit Delta Distribution is currently nominal.");
                }
            };

            chatToolbar.appendChild(clearBtn);
            chatToolbar.appendChild(logitBtn);

            const msnInputDiv = document.getElementById('msn-input');
            if (msnInputDiv && msnInputDiv.parentElement) {
                chatContainer.insertBefore(chatToolbar, msnInputDiv.parentElement);
            }
        }
    } catch (e) {
        console.error("Safe Chat Hook failed:", e); // Isolated error boundary
    }

    // --- 2. CLIPPY CONTROL PAD (Swarm Master Override) ---
    try {
        // Use a short delay to ensure clippy bubble exists
        setTimeout(() => {
            const clippyBubble = document.getElementById('clippy-bubble');
            if (clippyBubble && !document.getElementById('clippy-control-pad')) {
                const padContainer = document.createElement('div');
                padContainer.id = 'clippy-control-pad';
                padContainer.style.cssText = 'margin-top: 10px; border-top: 1px dashed #00ffff; padding-top: 5px; display: flex; flex-direction: column; gap: 3px;';
                
                padContainer.innerHTML = `
                    <div style="font-weight: bold; color: #ff00ff; text-align: center; font-size: 10px; margin-bottom: 2px;">[SWARM CONTROL PAD]</div>
                    <button id="clip-override-consensus" style="background: #ff0000; color: #fff; border: 1px solid #fff; font-size: 9px; cursor: pointer; padding: 2px;">BYPASS CONSENSUS</button>
                    <button id="clip-hot-patch" style="background: #ffaa00; color: #000; border: 1px solid #fff; font-size: 9px; cursor: pointer; padding: 2px;">FORCE HOT-PATCH (ECON)</button>
                    <button id="clip-purge" style="background: #000; color: #ff00ff; border: 1px solid #ff00ff; font-size: 9px; cursor: pointer; padding: 2px;">HALT DEPIN SWARM</button>
                `;

                clippyBubble.appendChild(padContainer);

                // Safe Event Delegation preventing bubble toggle
                document.getElementById('clip-override-consensus').addEventListener('click', (e) => {
                    e.stopPropagation();
                    if (window.showNotification) window.showNotification("MASTER OVERRIDE", "Swarm consensus bypassed. Direct logic execution authorized.", true);
                });

                document.getElementById('clip-hot-patch').addEventListener('click', (e) => {
                    e.stopPropagation();
                    if (window.showNotification) window.showNotification("HOT-PATCH EXECUTED", "Economy algorithm patched natively in memory.");
                });

                document.getElementById('clip-purge').addEventListener('click', (e) => {
                    e.stopPropagation();
                    if (window.showNotification) window.showNotification("SYS_HALT", "All DePIN agent operations physically frozen.", true);
                });
                
                clippyBubble.style.width = '240px'; // Re-style non-destructively
            }
        }, 500);
    } catch (e) {
        console.error("Clippy Control Pad Hook failed:", e);
    }

    // --- 3. URBAN HEAT ISLAND & SPRITEKIT HUD WIDGET ---
    try {
        if (!document.getElementById('urban-heat-hud')) {
            const hud = document.createElement('div');
            hud.id = 'urban-heat-hud';
            hud.style.cssText = 'position: absolute; top: 10px; right: 10px; background: rgba(0,0,0,0.8); color: #00ff00; border: 1px solid #00ff00; padding: 5px; font-size: 9px; font-family: "Courier New", monospace; z-index: 9999; pointer-events: none; text-shadow: 0 0 2px #00ff00; box-shadow: 0 0 5px #00ff00;';
            hud.innerHTML = `
                <div style="font-weight: bold; border-bottom: 1px dashed #0f0; margin-bottom: 3px; text-align: center;">[HUD] METROPOLIS METRICS</div>
                <div>CORE TEMP: <span style="color:#ffaa00;">42°C</span></div>
                <div>URBAN HEAT MITIGATION: <span style="color:#00ffff;">ACTIVE</span></div>
                <div>ALBEDO RATING: 0.85</div>
                <div>SSD IOPS: STABLE</div>
            `;
            document.body.appendChild(hud);
        }
    } catch (e) {
        console.error("HUD Widget Hook failed:", e);
    }
})();
