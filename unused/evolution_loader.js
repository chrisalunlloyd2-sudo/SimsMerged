// [EVOLUTIONARY LOADER]
// TIMESTAMP: 2026-05-27T19:40:00.000Z
// Dynamically pulls and executes advanced UI components from the Evolution Council.

async function loadEvolutionaryModules() {
    try {
        console.log("[EVOLUTION] Scanning for advanced UI modules...");
        const response = await fetch('http://localhost:8000/api/evolution-modules');
        const modules = await response.json();
        
        if (!modules || modules.length === 0) {
            console.log("[EVOLUTION] No new modules found. Environment stable.");
            return;
        }

        for (const moduleFile of modules) {
            const scriptPath = `js/evolution/${moduleFile}`;
            if (document.querySelector(`script[src="${scriptPath}"]`)) continue;

            console.log(`[EVOLUTION] Injecting module: ${moduleFile}`);
            const script = document.createElement('script');
            script.src = scriptPath;
            script.async = true;
            document.body.appendChild(script);
            
            if (window.showNotification) {
                window.showNotification("EVOLUTION_SYNC", `Injected advanced UI module: ${moduleFile}`);
            }
        }
    } catch (err) {
        console.error("[EVOLUTION_LOAD_ERR] Failed to load modules:", err);
    }
}

// Polling interval to check for new environmental components every 5 minutes
setInterval(loadEvolutionaryModules, 300000);
loadEvolutionaryModules();
