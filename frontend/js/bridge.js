async function SyncLoop() {
    try {
        // 1. Fetch Agents
        const agentResponse = await fetch('http://localhost:8000/api/agents');
        if (agentResponse.ok) {
            const agentData = await agentResponse.json();
            // Map and filter agents if necessary, ensuring they have positions
            window.agents = agentData.map(a => ({
                ...a,
                x: a.x || Math.random() * 20,
                y: a.y || Math.random() * 20,
                role: a.role || 'KERNEL'
            }));
        }

        // 2. Fetch Trajectories (Packet Flows)
        const trajectoryResponse = await fetch('http://localhost:8000/api/trajectories');
        if (trajectoryResponse.ok) {
            const trajectoryData = await trajectoryResponse.json();
            // We can use this to dynamically update the trajectories shown in engine.js
            // For now, let's assume engine.js can access a global 'activeLinks'
            window.activeLinks = trajectoryData;
        }

        // 3. Fetch Quantum Tick (System Health)
        let tickUrl = 'http://localhost:8000/api/quantum-tick';
        const researchTaskId = document.getElementById('research-task-id')?.value;
        if (researchTaskId) {
            tickUrl += `?task_id=\${researchTaskId}`;
        }

        const tickResponse = await fetch(tickUrl);
        if (tickResponse.ok) {
            const tickData = await tickResponse.json();
            window.systemStability = tickData.data.stability;
            window.systemCycle = tickData.data.tick;
            window.systemHeat = tickData.data.heat;
            window.systemFrequency = tickData.data.frequency;
            window.ramLoad = tickData.data.ram_load;
            window.isSwapping = tickData.data.is_swapping;
            window.casLatency = tickData.data.cas_latency;
            window.dirtyPages = tickData.data.dirty_pages || [];
            window.vramShadow = tickData.data.vram_shadow;
            window.coldPages = tickData.data.cold_pages || [];
            window.iopsLag = tickData.data.iops_lag;
            window.speculativeActive = tickData.data.speculative_execution;
            window.memPressure = tickData.data.memory_pressure;
            window.isRefreshing = tickData.data.is_refreshing;
            window.activeResearchAttrs = tickData.data.active_attrs;
            window.systemWeather = tickData.data.weather;
            window.cyberEconomy = tickData.data.economy;
            window.cityProgression = tickData.data.progression;
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

        // 5. Fetch Hardware Specs (Once)
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
                { name: "Sim (Local)", x: 5, y: 5, role: 'KERNEL' },
                { name: "Admin (Local)", x: 2, y: 2, role: 'ADMIN' }
            ];
        }
    }
}

// Start the loop
setInterval(SyncLoop, 1000);
SyncLoop();
