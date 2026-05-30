# TIMESTAMP: 2026-05-26T17:55:00.452Z
# PROJECT_ID: SimsMerged-v1.3-Metropolis
# AGENT_ID: Gemini-CLI-Architect

import sys
import os
import uvicorn

# Add the current directory to sys.path to ensure local imports work
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_root)

# Import the main app
from backend.main import app

if __name__ == "__main__":
    print("--- METROPOLIS AUTHORITY: HEADLESS MODE ---")
    print("GUI components bypassed. Browser auto-launch disabled.")
    print("Starting backend services on http://127.0.0.1:8000")
    
    # Run uvicorn without the browser launcher thread
    uvicorn.run(app, host="127.0.0.1", port=8000, log_level="info")
