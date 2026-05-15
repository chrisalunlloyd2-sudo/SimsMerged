async function sync() {
    try {
        // Try absolute URL since we might be running as file://
        const response = await fetch('http://localhost:8000/api/agents');
        if (!response.ok) throw new Error("Server not responding");
        const data = await response.json();
        
        // Add random positions for visual movement in the "Full Game"
        const mappedAgents = data.map(a => ({
            ...a,
            x: Math.random() * 10,
            y: Math.random() * 10,
            color: 'cyan'
        }));
        
        window.updateAgents(mappedAgents, "ONLINE (FASTAPI ACTIVE)");
    } catch (e) {
        // FALLBACK: Simulation mode if backend is down
        const mockAgents = [
            { name: "Sim (Local Simulation)", x: 5 + Math.sin(Date.now()/1000), y: 5 + Math.cos(Date.now()/1000), color: 'orange' },
            { name: "Agent (Local Simulation)", x: 2, y: 8, color: 'lime' }
        ];
        window.updateAgents(mockAgents, "LOCAL FALLBACK (Server Offline)");
    }
}

setInterval(sync, 1000);