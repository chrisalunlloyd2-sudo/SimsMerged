/**
 * [2026-05-17T18:05:00.000Z] [SimsMerged-v1.3-Metropolis] [Gemini-CLI-Architect]
 * METROPOLIS CYBER CONSOLE - REAL-TIME LOGGING INTERFACE
 */

(function() {
    /**
     * Appends timestamped messages to the cyber-console div.
     * @param {string} msg - The message to log.
     */
    window.logToCyberConsole = function(msg) {
        const consoleDiv = document.getElementById('cyber-console');
        if (!consoleDiv) return;

        const timestamp = new Date().toISOString().split('T')[1].split('.')[0];
        const logEntry = document.createElement('div');
        logEntry.style.borderBottom = '1px solid rgba(0, 255, 0, 0.1)';
        logEntry.style.padding = '2px 0';
        logEntry.innerHTML = `<span style="color: #888;">[${timestamp}]</span> ${msg}`;

        consoleDiv.appendChild(logEntry);
        consoleDiv.scrollTop = consoleDiv.scrollHeight;
        
        // Also log to the original console for parity
        if (window.logToConsole) {
            window.logToConsole(msg);
        }
    };

    console.log("[CyberConsole] Metropolis Logging Engine Online.");
})();
