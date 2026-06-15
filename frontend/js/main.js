/**
 * TIMESTAMP: 2026-06-09
 * PROJECT_ID: SimsMerged-v1.4.2
 * DESCRIPTION: Phase 1 - UI Binding & Initialization
 */

document.addEventListener('DOMContentLoaded', () => {
    // 1. Initialize Canvas Engine
    const engine = new IsometricEngine('isometric-canvas');
    
    // 2. Bind UI Elements to State
    const pulseIndicator = document.getElementById('pulse-indicator');
    const btnPause = document.getElementById('btn-pause');
    const btnSpawn = document.getElementById('btn-spawn');
    
    // Subscribe to state changes to update the DOM
    appState.subscribe((state) => {
        // Update Pulse
        if (state.systemStatus === 'ONLINE') {
            pulseIndicator.textContent = 'ONLINE';
            pulseIndicator.className = 'active';
            btnPause.textContent = 'PAUSE MATRIX';
        } else {
            pulseIndicator.textContent = 'PAUSED';
            pulseIndicator.className = 'paused';
            btnPause.textContent = 'RESUME MATRIX';
        }
    });

    // 3. UI Event Listeners
    btnPause.addEventListener('click', () => {
        const current = appState.getState().systemStatus;
        actions.setSystemStatus(current === 'ONLINE' ? 'PAUSED' : 'ONLINE');
    });

    btnSpawn.addEventListener('click', () => {
        // Mock Spawning an agent for UI testing
        const id = `AGENT_${Math.floor(Math.random() * 1000)}`;
        const startX = Math.floor(Math.random() * 10);
        const startY = Math.floor(Math.random() * 10);
        
        actions.upsertAgent(id, {
            x: startX, 
            y: startY, 
            z: 0, 
            balance: 20.0,
            status: 'ACTIVE'
        });
        
        // Mock a chat message
        const chatDiv = document.getElementById('chat-messages');
        const msg = document.createElement('div');
        msg.innerHTML = `<span style="color:var(--accent-green)">[System]</span> Spawned ${id} at Zone (${startX},${startY},0)`;
        chatDiv.appendChild(msg);
    });

    // Initial Test Setup
    console.log("SimsMerged Isometric Engine Initialized.");
});
