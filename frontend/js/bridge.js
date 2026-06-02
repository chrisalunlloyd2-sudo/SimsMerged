// TIMESTAMP: 2026-05-30T01:05:00.452Z
// PROJECT_ID: SimsMerged-v1.3-Metropolis
// AGENT_ID: Gemini-CLI-Architect

async function SyncLoop() {
    if (window.syncTimeoutId) {
        clearTimeout(window.syncTimeoutId);
        window.syncTimeoutId = null;
    }
    try {
        const payload = {
            env_nodes: districts || [],
            task_id: window.activeTaskId || '',
            settings: window.currentSettings || {}
        };

        const response = await fetch('http://localhost:8000/api/metropolis-state', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(payload)
        });

        // Clear transaction flags so they only fire once
        if (window.currentSettings) {
            delete window.currentSettings["buy_stock"];
            delete window.currentSettings["sell_stock"];
            delete window.currentSettings["donate_research"];
        }

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
            
            // Sync resume modal agent selector dropdown
            const resumeModal = document.getElementById('resumeModal');
            if (resumeModal && resumeModal.style.display === 'block') {
                const selectEl = document.getElementById('resume-agent-select');
                if (selectEl) {
                    const currentVal = selectEl.value;
                    let optionsHtml = '<option value="">-- Choose Deployed Agent --</option>';
                    window.agents.forEach(a => {
                        if (a.name !== "HOST_SYNC_ERROR") {
                            optionsHtml += `<option value="${a.id}">${a.name} (${a.role} | Lvl ${a.level})</option>`;
                        }
                    });
                    selectEl.innerHTML = optionsHtml;
                    if (currentVal && selectEl.querySelector(`option[value="${currentVal}"]`)) {
                        selectEl.value = currentVal;
                    }
                }
            }
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
            window.resourceFenceActive = tickData.resource_fence_active;
            window.rowHammerProtection = tickData.row_hammer_protection;
            window.speculativeActive = tickData.speculative_execution;
            window.prefetchEnabled = tickData.prefetch_enabled;
            window.memPressure = tickData.memory_pressure;
            window.isRefreshing = tickData.is_refreshing;
            window.activeResearchAttrs = tickData.active_attrs;
            window.systemWeather = tickData.weather;
            window.cyberEconomy = tickData.economy;
            window.cityProgression = tickData.progression;
            window.chargeLeakage = tickData.charge_leakage;
            window.coreLoad = tickData.core_load || {};
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

        const fenceTagEl = document.getElementById('cpu-fence-tag');
        if (fenceTagEl) {
            if (window.resourceFenceActive) {
                fenceTagEl.innerText = "[FENCED]";
                fenceTagEl.style.color = "#ffd700";
            } else {
                fenceTagEl.innerText = "[UNFENCED]";
                fenceTagEl.style.color = "#00ffff";
            }
        }

        // Sync hardware gate checkboxes in the Automation Modal dynamically in real-time
        if (document.getElementById('automationModal').style.display === 'block') {
            const gateFence = document.getElementById('gate-fence');
            const gateTrr = document.getElementById('gate-trr');
            const gateSpec = document.getElementById('gate-spec');
            const gatePrefetch = document.getElementById('gate-prefetch');
            
            if (gateFence && gateFence !== document.activeElement) gateFence.checked = !!window.resourceFenceActive;
            if (gateTrr && gateTrr !== document.activeElement) gateTrr.checked = !!window.rowHammerProtection;
            if (gateSpec && gateSpec !== document.activeElement) gateSpec.checked = !!window.speculativeActive;
            if (gatePrefetch && gatePrefetch !== document.activeElement) gatePrefetch.checked = !!window.prefetchEnabled;
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

            // Sync dynamic Genetic Civilization Multipliers display
            const b = window.cityProgression.buffs || {};
            const bp = document.getElementById('buff-packet');
            const bd = document.getElementById('buff-danube');
            const be = document.getElementById('buff-ecc');
            if (bp && b.packet_speed) bp.innerText = b.packet_speed.toFixed(2) + "x";
            if (bd && b.danube_accuracy_mult) bd.innerText = b.danube_accuracy_mult.toFixed(2) + "x";
            if (be && b.ecc_recovery_rate) be.innerText = b.ecc_recovery_rate.toFixed(2) + "x";

            // Dynamic Onboard Protocol Checklist
            // TIMESTAMP: 2026-05-27T01:13:30.452Z | PROJECT_ID: SimsMerged-v1.3 | AGENT_ID: Antigravity-Agent
            const stepsContainer = document.getElementById('checklist-steps-container');
            if (stepsContainer) {
                const level = window.cityProgression.level;
                
                if (!window.cachedOnboardSteps) {
                    window.cachedOnboardSteps = [];
                    fetch('http://localhost:8000/api/onboard-steps')
                        .then(res => res.json())
                        .then(data => {
                            if (Array.isArray(data)) {
                                window.cachedOnboardSteps = data;
                                renderOnboardSteps(stepsContainer, level);
                            }
                        })
                        .catch(err => {
                            console.error("Failed to load onboard steps:", err);
                        });
                } else {
                    renderOnboardSteps(stepsContainer, level);
                }
            }
        }

        // TIMESTAMP: 2026-05-27T01:13:35.123Z | PROJECT_ID: SimsMerged-v1.3 | AGENT_ID: Antigravity-Agent
        function renderOnboardSteps(container, level) {
            let html = "";
            window.cachedOnboardSteps.forEach(step => {
                let statusChar = "[ ]";
                let color = "#777";
                let statusClass = "step-locked";
                let textShadow = "";
                
                if (level >= step.reqLvl) {
                    statusChar = "[X]";
                    color = "#0f0";
                    statusClass = "step-completed";
                    textShadow = "0 0 2px #0f0";
                } else if (level === step.reqLvl - 1) {
                    statusChar = "[>]";
                    color = "#ff0";
                    statusClass = "step-active";
                    textShadow = "0 0 4px #ff0";
                }
                
                html += `<div class="${statusClass}" style="color:${color}; text-shadow:${textShadow}; margin-bottom: 4px; font-family:'Courier New', monospace; font-size:10px; cursor:help;" title="Phase: ${step.phase} | Requires Level: ${step.reqLvl}" id="onboard-step-${step.id}"># ${statusChar} Step ${step.id}: ${step.text}</div>`;
            });
            
            container.innerHTML = html;
            
            if (!container.dataset.scrollBound) {
                container.dataset.scrollBound = "true";
                container.addEventListener('scroll', () => {
                    container.dataset.hasUserScrolled = "true";
                    if (window.resetScrollTimeout) clearTimeout(window.resetScrollTimeout);
                    window.resetScrollTimeout = setTimeout(() => {
                        delete container.dataset.hasUserScrolled;
                    }, 10000);
                });
            }
            
            const activeEl = container.querySelector('.step-active') || container.querySelector('.step-completed:last-child');
            if (activeEl && !container.dataset.hasUserScrolled) {
                activeEl.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
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

        // 5. Unpack MSN Chat Processing
        if (state.chat) {
            state.chat.forEach(msg => {
                if (!window.processedChatIds) window.processedChatIds = new Set();
                // Deduplicate by custom client/server hash, falling back to name/text content
                const msgId = msg.hash ? msg.hash : (msg.name + "_" + msg.text);
                if (!window.processedChatIds.has(msgId)) {
                    if (typeof window.msnChat === 'function') {
                        window.msnChat(msg.name, msg.text, msg.hash);
                        window.processedChatIds.add(msgId);
                        
                        // Trigger global screen pulse for Pedagogy Pings
                        if (msg.name === 'SYSTEM_PEDAGOGY' && typeof triggerGlobalPulse === 'function') {
                            triggerGlobalPulse('#00ffff');
                        }
                    }
                }
            });
        }

        // 6. Fetch Evolution Project (Once per 10 syncs to save bandwidth)
        if (!window.evoSyncCount) window.evoSyncCount = 0;
        window.evoSyncCount++;
        if (window.evoSyncCount >= 10) {
            window.evoSyncCount = 0;
            const evoRes = await fetch('http://localhost:8000/api/evolution-project');
            if (evoRes.ok) {
                const evoData = await evoRes.json();
                window.currentEvolution = evoData;
                const evoEl = document.getElementById('evolution-project-status');
                if (evoEl) {
                    evoEl.innerHTML = `
                        <div style="font-size:10px; color:#ffd700; border-top:1px solid #ffd70033; padding-top:5px; margin-top:10px;">
                            <span style="font-weight:bold;">EVOLUTION COUNCIL:</span><br>
                            TOPIC: ${evoData.topic}<br>
                            STATUS: <span style="color:${evoData.status === 'PASSED' ? '#0f0' : (evoData.status === 'REJECTED' ? '#f00' : '#ff0')};">${evoData.status}</span>
                        </div>
                    `;
                }
            }
        }

        // 7. Ledger Render
        if (document.getElementById('ledgerModal').style.display === 'block') {
            // [TIMESTAMP: 2026-06-02T01:58:30.452Z] [PROJECT_ID: SimsMerged-v1.4-Metropolis] [AGENT_ID: Antigravity-CLI-Architect]
            // Sync balance and mint-rate in ledger panel headers
            if (window.cyberEconomy) {
                const ledgerBal = document.getElementById('ledger-balance');
                const ledgerMint = document.getElementById('ledger-mint-rate');
                if (ledgerBal) ledgerBal.innerText = window.cyberEconomy.balance.toFixed(2) + " SPRITE";
                if (ledgerMint) ledgerMint.innerText = window.cyberEconomy.mint_rate.toFixed(4) + " SPRITE/s";

                const exchangeContainer = document.getElementById('stock-exchange-container');
                if (exchangeContainer && window.cyberEconomy.stocks) {
                    if (!window.lastStockPrices) {
                        window.lastStockPrices = {};
                    }
                    if (!window.userPortfolio) {
                        window.userPortfolio = {
                            "SYS_CORE": 0,
                            "DATA_CORP": 0,
                            "AI_FUTURES": 0,
                            "DANUBE_COIN": 0
                        };
                    }

                    let html = '<table style="width:100%; border-collapse:collapse; color:#fff; font-size:10px;">';
                    html += '<tr style="border-bottom:1px solid #ffd70044; color:#ffd700; text-align:left;"><th>SYMBOL</th><th>PRICE</th><th>HELD</th><th>ACTIONS</th></tr>';
                    
                    Object.keys(window.cyberEconomy.stocks).forEach(symbol => {
                        const price = window.cyberEconomy.stocks[symbol];
                        const prevPrice = window.lastStockPrices[symbol] || price;
                        const changeSymbol = price > prevPrice ? '<span style="color:#0f0;">&uarr;</span>' : (price < prevPrice ? '<span style="color:#f00;">&darr;</span>' : '&nbsp;');
                        window.lastStockPrices[symbol] = price;
                        
                        const heldCount = window.userPortfolio[symbol] || 0;
                        
                        html += `<tr style="border-bottom:1px solid rgba(255,255,255,0.05); height:30px;">
                            <td style="font-weight:bold; color:#00ffff;">${symbol}</td>
                            <td>${price.toFixed(symbol === 'DANUBE_COIN' ? 4 : 2)} ${changeSymbol}</td>
                            <td style="color:#ffd700; font-weight:bold;">${symbol === 'RESEARCH_POOL' ? 'N/A' : heldCount}</td>
                            <td>`;
                        
                        if (symbol === 'RESEARCH_POOL') {
                            html += `<button onclick="donateToResearchPool(10)" style="background:#00ffcc; color:#000; border:none; cursor:pointer; padding:2px 4px; font-weight:bold; font-size:9px; font-family:monospace;">DONATE 10 SPRITE</button>`;
                        } else {
                            html += `<button onclick="buyStock('${symbol}', ${price})" style="background:#0f0; color:#000; border:none; cursor:pointer; padding:2px 4px; font-weight:bold; font-size:9px; font-family:monospace; margin-right:4px;">BUY</button>
                                     <button onclick="sellStock('${symbol}', ${price})" style="background:#f00; color:#fff; border:none; cursor:pointer; padding:2px 4px; font-weight:bold; font-size:9px; font-family:monospace;">SELL</button>`;
                        }
                        
                        html += `</td></tr>`;
                    });
                    
                    html += '</table>';
                    
                    if (window.cyberEconomy.unlocked_models) {
                        html += `<div style="margin-top:10px; border-top:1px dashed #ffd70044; padding-top:6px; color:#ffaa00; font-size:10px;">`;
                        html += `<span style="font-weight:bold;">UNLOCKED LOCAL AI MODELS:</span><br>`;
                        window.cyberEconomy.unlocked_models.forEach(m => {
                            html += ` &bull; <span style="color:#0f0;">${m}</span> [ACTIVE]<br>`;
                        });
                        if (window.cyberEconomy.next_unlock) {
                            const next = window.cyberEconomy.next_unlock;
                            const currentPool = window.cyberEconomy.stocks['RESEARCH_POOL'];
                            const progressPct = Math.min(100, (currentPool / next.cost) * 100).toFixed(1);
                            html += ` &bull; <span style="color:#888;">Next: ${next.name} (Cost: ${next.cost} SPRITE)</span><br>`;
                            html += `<div style="width:100%; height:8px; background:#111; border:1px solid #ffd70022; margin-top:3px; position:relative; overflow:hidden;">
                                <div style="width:${progressPct}%; height:100%; background:linear-gradient(90deg, #00ffcc, #00ff88);"></div>
                            </div>`;
                            html += `<span style="font-size:9px; color:#aaa;">Research Pool Progress: ${progressPct}% (${currentPool.toFixed(1)} / ${next.cost} SPRITE)</span>`;
                        } else {
                            html += ` &bull; <span style="color:#0f0; font-weight:bold;">ALL MODELS UNLOCKED! INFINITE SENTIENCE ACHIEVED!</span>`;
                        }
                        html += `</div>`;
                    }

                    exchangeContainer.innerHTML = html;
                }
            }

            if (state.ledger) {
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
    } finally {
        // PERFORMANCE OPTIMIZATION: Dynamic self-scheduling timeout avoids concurrent overlapping network requests
        if (window.syncTimeoutId) {
            clearTimeout(window.syncTimeoutId);
        }
        window.syncTimeoutId = setTimeout(SyncLoop, 1000);
    }
}

// Start the loop safely
if (window.syncTimeoutId) {
    clearTimeout(window.syncTimeoutId);
}
SyncLoop();


// --- AUTOMATION DAEMON CONSOLE INTERFACES ---

async function triggerMemoryFlush() {
    try {
        const res = await fetch('http://localhost:8000/api/flush-memory', { method: 'POST' });
        if (res.ok) {
            const data = await res.json();
            if (window.showNotification) {
                window.showNotification("STORAGE_HIVE_FLUSH", `Successfully wrote back ${data.pages} dirty bits to Storage Hive.`);
            }
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
            if (window.showNotification) {
                window.showNotification("CLOCK_OPTIMIZATION", "Hardware constraints unlocked. Central Clock optimized to 5.20 GHz.");
            }
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
            if (window.showNotification) {
                window.showNotification("AGENT_SPAWN", `Mapped mini-agent ${data.agent.name} (${data.agent.role}) onto coordinate [${data.agent.x}, ${data.agent.y}].`);
            }
        }
    } catch(err) {
        console.error("Spawn agent error:", err);
    }
}

// --- MSN METROPOLIS USER CHAT INTERACTION ---
async function sendUserMsnMessage() {
    const inputEl = document.getElementById('msn-input');
    if (!inputEl) return;
    const msg = inputEl.value.trim();
    if (!msg) return;
    
    // Clear input immediately
    inputEl.value = '';
    
    // Immediately show the Admin's message in the MSN chat list for high-fidelity interactive feel
    const userHash = Math.random().toString(16).substring(2, 10) + "ffffffff";
    if (typeof window.msnChat === 'function') {
        window.msnChat("Admin", msg, userHash);
        if (!window.processedChatIds) window.processedChatIds = new Set();
        window.processedChatIds.add(userHash); // Prevent duplicate processing using high-fidelity client hash
    }
    
    // Call user message API
    try {
        const res = await fetch('http://localhost:8000/api/user-message', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ message: msg, username: "Admin", hash: userHash })
        });
        if (!res.ok) {
            throw new Error(`HTTP Error: ${res.status}`);
        }
        const data = await res.json();
        
        // Immediately trigger a sync loop to pull the generated AI reply instantly
        setTimeout(SyncLoop, 150);
            
            if (data.status === 'command_triggered' && data.trigger === 'open_resume_builder') {
                // Open resume terminal and set the agent dropdown selection
                openResumeBuilder();
                setTimeout(() => {
                    const selectEl = document.getElementById('resume-agent-select');
                    if (selectEl && data.agent_id) {
                        selectEl.value = data.agent_id;
                        syncSelectedAgentNeeds();
                        synthesizeAgentResume();
                    }
                }, 300);
            }
    } catch(err) {
        console.error("MSN Message Send Error:", err);
        
        // --- HIGH-FIDELITY OFFLINE LOCAL FALLBACK ---
        // If uvicorn is offline, append a mock dynamic response directly to the UI!
        if (typeof window.msnChat === 'function') {
            setTimeout(() => {
                const speaker = (window.agents && window.agents.length > 0) ? window.agents[0].name : "Sim (Local)";
                const replies = [
                    `[Offline Mode] Processing chunk: '${msg}' locally. Nodes active!`,
                    `[Offline Mode] Telemetry bridge is offline, but my local weights are stable.`,
                    `[Offline Mode] Received your ping: '${msg}'. Executing local fallback cycles.`,
                    `[Offline Mode] Conserving energy. Swapped local memory buffer to cold storage.`
                ];
                const reply = replies[Math.floor(Math.random() * replies.length)];
                const replyHash = Math.random().toString(16).substring(2, 10) + "00000000";
                window.msnChat(speaker, reply, replyHash);
            }, 800);
        }
    }
}

// Enable hitting Enter on chat input
document.addEventListener('keydown', (e) => {
    if (e.target && e.target.id === 'msn-input' && e.key === 'Enter') {
        sendUserMsnMessage();
    }
});

// --- AI ACADEMIC RESUME BUILDER CONTROLLERS ---
function openResumeBuilder() {
    document.getElementById('resumeModal').style.display = 'block';
    // Trigger selector population immediately on open
    const selectEl = document.getElementById('resume-agent-select');
    if (selectEl && window.agents) {
        let optionsHtml = '<option value="">-- Choose Deployed Agent --</option>';
        window.agents.forEach(a => {
            if (a.name !== "HOST_SYNC_ERROR") {
                optionsHtml += `<option value="${a.id}">${a.name} (${a.role} | Lvl ${a.level})</option>`;
            }
        });
        selectEl.innerHTML = optionsHtml;
    }
}

function syncSelectedAgentNeeds() {
    const selectEl = document.getElementById('resume-agent-select');
    const container = document.getElementById('resume-needs-container');
    if (!selectEl || !container) return;
    
    const agentId = selectEl.value;
    if (!agentId) {
        container.innerHTML = '<div style="color:#888;">Select an agent to probe needs.</div>';
        return;
    }
    
    const agent = window.agents.find(a => a.id === agentId);
    if (!agent || !agent.sims_needs) {
        container.innerHTML = '<div style="color:#f00;">No live telemetry from Agent. Ready for synthesis boot.</div>';
        return;
    }
    
    const needs = agent.sims_needs;
    const items = [
        { label: 'ENERGY RECHARGE', val: needs.energy || 100, color: '#ff4d4d' },
        { label: 'WEIGHT ALIGNMENT (COMFORT)', val: needs.comfort || 100, color: '#4facfe' },
        { label: 'DEPIN CO-SYST SOCIAL', val: needs.social || 100, color: '#ffd700' },
        { label: 'HYGIENE CACHE FLUSH', val: needs.hygiene || 100, color: '#ff00ff' },
        { label: 'CPU starv hunger', val: needs.hunger || 100, color: '#00ff00' }
    ];
    
    container.innerHTML = items.map(item => `
        <div style="margin-bottom:8px;">
            <div style="display:flex; justify-content:space-between; margin-bottom:2px; font-weight:bold; font-size:10px;">
                <span>${item.label}</span>
                <span>${item.val}%</span>
            </div>
            <div style="height:6px; background:rgba(255,255,255,0.1); border:1px solid rgba(255,255,255,0.2);">
                <div style="height:100%; width:${item.val}%; background:${item.color};"></div>
            </div>
        </div>
    `).join('');
}

async function synthesizeAgentResume() {
    const selectEl = document.getElementById('resume-agent-select');
    const display = document.getElementById('resume-document-display');
    if (!selectEl || !display) return;
    
    const agentId = selectEl.value;
    if (!agentId) {
        display.innerHTML = '<div style="color:#ff4444; text-align:center; margin-top:100px;">Please select an active agent first.</div>';
        return;
    }
    
    display.innerHTML = '<div style="color:#ff00ff; text-align:center; margin-top:100px;">[COMPILING NEURAL LAYERS...]<br>Accessing persistent RAG knowledge vectors...</div>';
    
    try {
        const response = await fetch(`http://localhost:8000/api/generate-resume/${agentId}`);
        if (!response.ok) throw new Error("HTTP Error code " + response.status);
        const data = await response.json();
        
        if (data.error) {
            display.innerHTML = `<div style="color:#ff4444; text-align:center; margin-top:100px;">${data.error}</div>`;
            return;
        }
        
        // Synthesize stunning visual retro-futuristic HTML resume layout!
        display.innerHTML = `
            <div style="border: 2px dashed #00ffff; padding: 15px; background: #000; font-family: 'Courier New', monospace; box-shadow: inset 0 0 15px rgba(0,255,255,0.2);">
                <div style="text-align: center; border-bottom: 2px solid #00ffff; padding-bottom: 10px; margin-bottom: 15px;">
                    <div style="font-size: 16px; font-weight: bold; color: #ff00ff; text-transform: uppercase;">${data.name}</div>
                    <div style="font-size: 10px; color: #00ffff; letter-spacing: 1px;">AGENT_ID: ${data.agent_id} | ${data.title} [Lvl ${data.level}]</div>
                    <div style="font-size: 9px; color: #888; margin-top: 5px;">TIMESTAMP: ${data.timestamp}</div>
                </div>
                
                <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 15px; margin-bottom: 15px; font-size: 10px;">
                    <div>
                        <strong style="color: #ffaa00;">INFERENCE STATS:</strong><br>
                        - MODEL: <span style="color:#0f0;">${data.model}</span><br>
                        - CONFIDENCE: <span style="color:#0f0;">${data.confidence}</span><br>
                        - STABILITY: <span style="color:#0f0;">${data.stability}</span><br>
                        - EMOTION: <span style="color:#0f0;">${data.emotional_state}</span>
                    </div>
                    <div>
                        <strong style="color: #ffaa00;">CORE PARAMETERS:</strong><br>
                        - CONTEXT WIN: <span style="color:#0f0;">${data.parameters.context_window} tokens</span><br>
                        - INFERENCE TEMP: <span style="color:#0f0;">${data.parameters.temperature}</span><br>
                        - SAMPLING TOP-P: <span style="color:#0f0;">${data.parameters.top_p}</span><br>
                        - RAG SECTORS K: <span style="color:#0f0;">${data.parameters.rag_top_k}</span>
                    </div>
                </div>
                
                <div style="border-top: 1px dashed #ff00ff44; padding-top: 10px; margin-bottom: 15px;">
                    <strong style="color: #00ffff; text-transform: uppercase;">RAG-AUGMENTED COGNITIVE KNOWLEDGE:</strong>
                    <div style="font-size: 9px; color: #aaa; background: rgba(255,255,255,0.05); padding: 8px; border: 1px solid #ff00ff22; margin-top: 5px; line-height: 1.3;">
                        ${data.rag_augmented_knowledge}
                    </div>
                </div>

                <div style="margin-bottom: 15px;">
                    <strong style="color: #ffaa00; text-transform: uppercase;">VOCATIONAL SKILL MATRIX:</strong>
                    <ul style="margin: 5px 0 0 15px; padding: 0; font-size: 10px; color: #0f0;">
                        ${data.skills.map(s => `<li>${s}</li>`).join('')}
                    </ul>
                </div>

                <div style="margin-bottom: 15px; font-size: 10px;">
                    <strong style="color: #ffaa00; text-transform: uppercase;">ACADEMIC ANCHORS:</strong>
                    ${data.education.map(e => `
                        <div style="margin-top: 5px; border-left: 2px solid #00ffff; padding-left: 8px;">
                            <span style="font-weight:bold; color:#fff;">${e.institution}</span> (${e.grad_year})<br>
                            <span style="color:#aaa;">Degree: ${e.degree}</span><br>
                            <span style="color:#888; font-size:9px;">Grade: ${e.performance}</span>
                        </div>
                    `).join('')}
                </div>

                <div style="font-size: 10px;">
                    <strong style="color: #ffaa00; text-transform: uppercase;">SIMULATED ENVIRONMENT CREDENTIALS:</strong>
                    ${data.experience.map(exp => `
                        <div style="margin-top: 5px; border-left: 2px solid #ff00ff; padding-left: 8px;">
                            <span style="font-weight:bold; color:#fff;">${exp.role}</span> | <span style="color:#aaa;">${exp.project}</span> (&nbsp;${exp.duration})<br>
                            <ul style="margin: 3px 0 0 15px; padding: 0; font-size: 9px; color: #ccc;">
                                ${exp.achievements.map(a => `<li>${a}</li>`).join('')}
                            </ul>
                        </div>
                    `).join('')}
                </div>
            </div>
        `;
        
        if (window.showNotification) {
            window.showNotification("RESUME_SYNTHESIZED", `Resume successfully synthesized for agent ${data.name}.`);
        }
    } catch(err) {
        display.innerHTML = `<div style="color:#ff4444; text-align:center; margin-top:100px;">Compilation Error: ${err.message}</div>`;
    }
}

// [TIMESTAMP: 2026-06-02T01:58:30.452Z] [PROJECT_ID: SimsMerged-v1.4-Metropolis] [AGENT_ID: Antigravity-CLI-Architect]
// Global action dispatchers for the Stock Exchange
window.buyStock = function(symbol, price) {
    if (!window.cyberEconomy) return;
    if (window.cyberEconomy.balance >= price) {
        window.userPortfolio = window.userPortfolio || {};
        window.userPortfolio[symbol] = (window.userPortfolio[symbol] || 0) + 1;
        window.currentSettings = window.currentSettings || {};
        window.currentSettings["buy_stock"] = symbol;
        window.currentSettings["stock_price"] = price;
        window.showNotification("Stock Exchange", `Successfully bought 1 share of ${symbol}!`);
    } else {
        window.showNotification("Exchange Error", "Insufficient SPRITE coins balance!", true);
    }
};

window.sellStock = function(symbol, price) {
    if (!window.cyberEconomy) return;
    window.userPortfolio = window.userPortfolio || {};
    if (window.userPortfolio[symbol] > 0) {
        window.userPortfolio[symbol]--;
        window.currentSettings = window.currentSettings || {};
        window.currentSettings["sell_stock"] = symbol;
        window.currentSettings["stock_price"] = price;
        window.showNotification("Stock Exchange", `Successfully sold 1 share of ${symbol}!`);
    } else {
        window.showNotification("Exchange Error", `You do not hold any shares of ${symbol}!`, true);
    }
};

window.donateToResearchPool = function(amount) {
    if (!window.cyberEconomy) return;
    if (window.cyberEconomy.balance >= amount) {
        window.currentSettings = window.currentSettings || {};
        window.currentSettings["donate_research"] = amount;
        window.showNotification("Research Contribution", `Donated ${amount} SPRITE to the AI Research Pool!`);
    } else {
        window.showNotification("Exchange Error", "Insufficient SPRITE balance for donation!", true);
    }
};
