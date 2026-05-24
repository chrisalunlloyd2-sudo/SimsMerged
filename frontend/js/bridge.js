// TIMESTAMP: 2026-05-23T04:05:00Z
// PROJECT_ID: SimsMerged-v1.3
// AGENT_ID: Antigravity-Architect

async function SyncLoop() {
    try {
        const payload = {
            env_nodes: districts || [],
            task_id: window.activeTaskId || ''
        };

        const response = await fetch('http://localhost:8000/api/metropolis-state', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(payload)
        });

        if (!response.ok) {
            throw new Error(`HTTP Error: ${response.status}`);
        }

        const state = await response.json();

        // 1. Unpack Agents
        if (state.agents) {
            window.agents = state.agents.map(a => ({
                ...a,
                x: a.x || Math.random() * 20,
                y: a.y || Math.random() * 20,
                role: a.role || 'KERNEL'
            }));
        }

        // 2. Unpack Trajectories
        if (state.trajectories) {
            window.activeLinks = state.trajectories;
        }

        // 3. Unpack Quantum Tick (System Health)
        if (state.quantum_tick) {
            const tickData = state.quantum_tick;
            window.systemStability = tickData.stability;
            window.systemCycle = tickData.tick;
            window.systemHeat = tickData.heat;
            window.systemFrequency = tickData.frequency;
            window.ramLoad = tickData.ram_load;
            window.isSwapping = tickData.is_swapping;
            window.casLatency = tickData.cas_latency;
            window.dirtyPages = tickData.dirty_pages || [];
            window.vramShadow = tickData.vram_shadow;
            window.coldPages = tickData.cold_pages || [];
            window.iopsLag = tickData.iops_lag;
            window.speculativeActive = tickData.speculative_execution;
            window.memPressure = tickData.memory_pressure;
            window.isRefreshing = tickData.is_refreshing;
            window.activeResearchAttrs = tickData.active_attrs;
            window.systemWeather = tickData.weather;
            window.cyberEconomy = tickData.economy;
            window.cityProgression = tickData.progression;
            window.chargeLeakage = tickData.charge_leakage;
        }

        // 4. Update UI labels
        if (window.updateStatus) {
            window.updateStatus("SYNCED: METROPOLIS ACTIVE");
        }

        const clockEl = document.getElementById('cpu-clock');
        if (clockEl && window.systemFrequency) {
            clockEl.innerText = (window.systemFrequency * (window.systemFrequency < 100 ? 1 : 0.001)).toFixed(2) + " GHz";
            if (window.systemHeat > 80) clockEl.style.color = '#f00';
            else clockEl.style.color = '#0f0';
        }
        
        const weatherEl = document.getElementById('env-weather');
        if (weatherEl && window.systemWeather) {
            weatherEl.innerText = window.systemWeather;
            if (window.systemWeather.includes("STORM") || window.systemWeather.includes("CORRUPTION")) {
                weatherEl.style.color = '#f00';
            } else {
                weatherEl.style.color = '#0ff';
            }
        }
        
        const mintRateEl = document.getElementById('mint-rate');
        const cryptoBalEl = document.getElementById('crypto-balance');
        if (window.cyberEconomy) {
            if (mintRateEl) mintRateEl.innerText = window.cyberEconomy.mint_rate.toFixed(2) + " SPRITE/s";
            if (cryptoBalEl) cryptoBalEl.innerText = window.cyberEconomy.balance.toFixed(2);
        }
        
        const lvlEl = document.getElementById('city-level');
        const xpEl = document.getElementById('city-xp');
        const unlockEl = document.getElementById('city-unlock');
        if (window.cityProgression) {
            if (lvlEl) lvlEl.innerText = window.cityProgression.level;
            if (xpEl) xpEl.innerText = window.cityProgression.progress_pct;
            if (unlockEl && window.cityProgression.recent_unlocks && window.cityProgression.recent_unlocks.length > 0) {
                const recent = window.cityProgression.recent_unlocks;
                unlockEl.innerText = recent[recent.length - 1];
            }
        }

        // 5. MSN Chat Processing
        if (state.chat) {
            state.chat.forEach(msg => {
                if (!window.processedChatIds) window.processedChatIds = new Set();
                const msgId = msg.name + msg.time;
                if (!window.processedChatIds.has(msgId)) {
                    window.msnChat(msg.name, msg.text, msg.hash);
                    window.processedChatIds.add(msgId);
                }
            });
        }

        // 6. Ledger Render
        if (document.getElementById('ledgerModal').style.display === 'block' && state.ledger) {
            const content = document.getElementById('ledger-content');
            content.innerHTML = state.ledger.map(t => `
                <div style="margin-bottom:5px; border-bottom:1px solid #040;">
                    <span style="color:#888;">[${new Date(t.timestamp * 1000).toLocaleTimeString()}]</span> 
                    <span style="color:#fff;">AGENT: ${t.agent}</span> | 
                    <span style="color:#0f0;">ACTION: ${t.action}</span><br>
                    <span style="color:#444; font-size:9px;">HASH: ${t.hash}</span>
                </div>
            `).join('');
            content.scrollTop = content.scrollHeight;
        }

        // 7. Fetch Hardware Specs (Once)
        if (!window.hardwareSpecs) {
            const hardwareResponse = await fetch('http://localhost:8000/api/hardware');
            if (hardwareResponse.ok) {
                window.hardwareSpecs = await hardwareResponse.json();
                console.log("HARDWARE_SYNC: Real nominal values loaded.");
            }
        }

    } catch (e) {
        console.error("Telemetry Bridge Error:", e);
        if (window.updateStatus) {
            window.updateStatus("OFFLINE: LOCAL SIMULATION");
        }
        
        // Fallback mock data
        if (!window.agents || window.agents.length === 0) {
            window.agents = [
                { name: "Sim (Local)", x: 5, y: 5, level: 1, title: 'Kernel Node', role: 'KERNEL' },
                { name: "Admin (Local)", x: 2, y: 2, level: 5, title: 'Root Domain', role: 'ADMIN' }
            ];
        }
    }
}

// Start the loop
setInterval(SyncLoop, 1000);
SyncLoop();
