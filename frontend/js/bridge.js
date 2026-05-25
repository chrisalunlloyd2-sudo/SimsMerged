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

            // Dynamic Onboard Protocol Checklist
            const checklistEl = document.getElementById('protocol-checklist');
            if (checklistEl) {
                const level = window.cityProgression.level;
                
                let html = `<div style="color:#00ffff; font-weight:bold; border-bottom: 1px solid #00ffff; margin-bottom: 5px; padding-bottom: 3px;">100-STEP ONBOARD PROTOCOL</div>`;
                
                const steps = [
                    { id: 1, text: "Genesis Restoration", reqLvl: 1 },
                    { id: 2, text: "UI Interactivity Fix", reqLvl: 2 },
                    { id: 3, text: "Resource Fencing", reqLvl: 3 },
                    { id: 4, text: "Dynamic Swarms Spawning", reqLvl: 4 },
                    { id: 5, text: "Hashed Chunk Verification", reqLvl: 5 }
                ];
                
                steps.forEach(step => {
                    let statusChar = "[ ]";
                    let color = "#888";
                    if (level >= step.reqLvl) {
                        statusChar = "[X]";
                        color = "#0f0";
                    } else if (level === step.reqLvl - 1) {
                        statusChar = "[>]";
                        color = "#ff0";
                    }
                    html += `<div style="color:${color};"># ${statusChar} Step ${step.id}: ${step.text}</div>`;
                });
                
                const remaining = Math.max(0, 100 - level);
                html += `<div style="color:#888; margin-top: 5px;">... ${remaining} Steps Remaining ...</div>`;
                checklistEl.innerHTML = html;
            }
        }

        // Render Automation Modal Fleet when displayed
        if (document.getElementById('automationModal').style.display === 'block' && state.agents) {
            const fleetContainer = document.getElementById('fleet-container');
            if (fleetContainer) {
                fleetContainer.innerHTML = state.agents.map(a => `
                    <div style="margin-bottom: 8px; border-bottom: 1px dashed #00ffff33; padding-bottom: 4px;">
                        <span style="color:#ffd700; font-weight:bold;">${a.name}</span> 
                        <span style="color:#888;">(${a.role})</span><br>
                        <span>LEVEL: ${a.level} [${a.title}]</span> | 
                        <span>STATE: <span style="color:${a.state === 'STABLE' ? '#0f0' : '#f00'};">${a.state}</span></span><br>
                        <span>LAST ACTION: <span style="color:#0ff;">${a.last_action}</span></span> | 
                        <span>CONFIDENCE: ${(a.confidence * 100).toFixed(0)}%</span><br>
                        <span style="color:#555; font-size:9px;">HASH: ${a.last_hash ? a.last_hash.substring(0,24) : '00000000'}...</span>
                    </div>
                `).join('');
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

// --- AUTOMATION DAEMON CONSOLE INTERFACES ---

async function triggerMemoryFlush() {
    try {
        const res = await fetch('http://localhost:8000/api/flush-memory', { method: 'POST' });
        if (res.ok) {
            const data = await res.json();
            alert(`[FLUSH_SUCCESS] Successfully wrote back ${data.pages} dirty bits to Storage Hive.`);
        }
    } catch(err) {
        console.error("Flush memory error:", err);
    }
}

async function triggerClockOptimization() {
    try {
        const res = await fetch('http://localhost:8000/api/configure-core', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ cpu_throttle_limit: 1.0, resource_fence_active: false })
        });
        if (res.ok) {
            alert(`[OPTIMIZE_SUCCESS] Hardware constraints unlocked. Central Clock optimized to 5.20 GHz.`);
            const fenceChk = document.getElementById('gate-fence');
            if (fenceChk) fenceChk.checked = false;
        }
    } catch(err) {
        console.error("Clock optimization error:", err);
    }
}

async function updateCoreGate(gateName, value) {
    try {
        const payload = {};
        payload[gateName] = value;
        
        await fetch('http://localhost:8000/api/configure-core', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(payload)
        });
    } catch(err) {
        console.error("Core gate error:", err);
    }
}

async function deployMiniAgent() {
    const name = document.getElementById('spawn-name').value || "Swarm_Bot";
    const role = document.getElementById('spawn-role').value || "PROCESS_KERNEL";
    const x = parseInt(document.getElementById('spawn-x').value) || 2;
    const y = parseInt(document.getElementById('spawn-y').value) || 2;
    
    try {
        const res = await fetch('http://localhost:8000/api/spawn-agent', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ name, role, x, y })
        });
        if (res.ok) {
            const data = await res.json();
            alert(`[AGENT_SPAWNED] Mapped mini-agent ${data.agent.name} (${data.agent.role}) onto coordinate [${data.agent.x}, ${data.agent.y}].`);
        }
    } catch(err) {
        console.error("Spawn agent error:", err);
    }
}
