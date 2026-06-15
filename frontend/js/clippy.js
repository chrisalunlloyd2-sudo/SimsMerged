// Clippy-Metropolis: Lightweight Heuristic Assistant
// TIMESTAMP: 2026-05-31T20:25:00.000Z
// AGENT_ID: Gemini-CLI-Architect

(function() {
    const clippy = {
        element: null,
        bubble: null,
        currentTip: "",
        lastLagCheck: Date.now(),
        isOptimizing: false,

        init() {
            this.createUI();
            this.startHeuristics();
            this.showTip("Welcome to Metropolis! I'm Clippy, your system mediator. Need help finishing the install?");
        },

        createUI() {
            const container = document.createElement('div');
            container.id = 'clippy-container';
            container.style.cssText = 'position: fixed; bottom: 20px; right: 20px; z-index: 10000; cursor: pointer; transition: transform 0.3s;';
            
            const sprite = document.createElement('div');
            sprite.innerHTML = '📎'; // Paperclip emoji as base
            sprite.style.cssText = 'font-size: 50px; filter: drop-shadow(0 0 5px #00ffff);';
            
            const bubble = document.createElement('div');
            bubble.id = 'clippy-bubble';
            bubble.style.cssText = 'position: absolute; bottom: 60px; right: 0; width: 200px; background: #001a1a; border: 1px solid #00ffff; padding: 10px; color: #00ffff; font-family: "Courier New", monospace; font-size: 12px; display: none; box-shadow: 0 0 15px rgba(0,255,255,0.3);';
            
            container.appendChild(bubble);
            container.appendChild(sprite);
            document.body.appendChild(container);

            this.element = container;
            this.bubble = bubble;

            container.addEventListener('click', () => this.toggleBubble());
            container.addEventListener('mouseenter', () => container.style.transform = 'scale(1.1)');
            container.addEventListener('mouseleave', () => container.style.transform = 'scale(1.0)');
        },

        showTip(text) {
            this.currentTip = text;
            this.bubble.innerHTML = text;
            this.bubble.style.display = 'block';
            setTimeout(() => {
                if (this.currentTip === text) this.bubble.style.display = 'none';
            }, 8000);
        },

        toggleBubble() {
            this.bubble.style.display = (this.bubble.style.display === 'none') ? 'block' : 'none';
        },

        startHeuristics() {
            setInterval(() => {
                this.checkSystemHealth();
            }, 5000); // Check every 5 seconds
        },

        checkSystemHealth() {
            // Heuristic: Check global window variables populated by bridge.js
            if (window.systemHeat > 85) {
                this.showTip("Hey! I noticed your core is running HOT! Want me to trigger a thermal purge?");
            } else if (window.systemStability < 0.4) {
                this.showTip("Stability is dropping! I suggest deploying a DOCTOR agent to Sector 0 immediately.");
            } else if (window.isSwapping) {
                this.showTip("Your system is swapping to disk! This causes major lag. Should I flush the memory dirty pages?");
            } else if (window.cityProgression && window.cityProgression.level < 5) {
                this.showTip("New here? Try dragging a 'Crate' (file) into a 'Mining Zone' to get started!");
            }
            
            // Check for install completeness
            if (!window.agents || window.agents.length === 0) {
                this.showTip("I noticed no agents are deployed. Use the 'Spawn' tool to bring the city to life!");
            }
        },

        async triggerOptimization(type) {
            this.isOptimizing = true;
            this.showTip(`Optimizing ${type}... Please wait...`);
            
            if (type === 'thermal') {
                await fetch('http://localhost:8000/api/configure-core', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ cpu_throttle_limit: 0.5 })
                });
            } else if (type === 'memory') {
                await fetch('http://localhost:8000/api/flush-memory', { method: 'POST' });
            }
            
            setTimeout(() => {
                this.showTip(`${type.toUpperCase()} optimization complete! System is now more stable.`);
                this.isOptimizing = false;
            }, 2000);
        }
    };

    window.clippy = clippy;
    clippy.init();
})();
