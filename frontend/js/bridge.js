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
            window.activeResearchAttrs = tickData.data.active_attrs;
        }

        // 4. Update UI labels
        if (window.updateStatus) {
            window.updateStatus("SYNCED: METROPOLIS ACTIVE");
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
