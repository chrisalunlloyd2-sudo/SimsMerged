# TIMESTAMP: 2026-05-23T03:31:00Z
# PROJECT_ID: SimsMerged-v1.3
# AGENT_ID: Antigravity-Architect

import sys
import os
import threading
import time
import webbrowser

# Add the current directory to sys.path
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_root)

# Import and run the main app
from backend.main import app
import uvicorn

def auto_launch_browser():
    """Closes old browser tabs/windows and opens the SimsMerged city frontend."""
    time.sleep(2.5)
    print("[GENESIS] Purging previous SimsMerged browser windows...")
    try:
        # Kills browser windows containing "SimsMerged" in the window title
        os.system('taskkill /F /FI "WINDOWTITLE eq SimsMerged*" >nul 2>&1')
    except Exception as err:
        pass

    frontend_path = os.path.abspath(os.path.join(project_root, "frontend", "index.html"))
    print(f"[GENESIS] Launching fresh UI at file:///{frontend_path}...")
    webbrowser.open(f"file:///{frontend_path}")

if __name__ == "__main__":
    # Start the auto-launch thread
    launcher_thread = threading.Thread(target=auto_launch_browser, daemon=True)
    launcher_thread.start()

    uvicorn.run(app, host="127.0.0.1", port=8000)
