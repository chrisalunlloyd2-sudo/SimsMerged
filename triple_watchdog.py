# [TIMESTAMP: 2026-06-08T05:30:00.000Z] [PROJECT_ID: SimsMerged-v1.4.2] [AGENT_ID: viper_cli-architectssj4]

import subprocess
import time
import os
import sys
import psutil
import random

# PATHS
BACKEND_MAIN = "C:\\Users\\viper\\Desktop\\SimsMerged\\backend\\main.py"
PYTHON_EXE = "C:\\Users\\viper\\python\\python.exe"
LOG_FILE = "C:\\Users\\viper\\Desktop\\SimsMerged\\SSD_SANDBOX\\watchdog.log"
STABILITY_LOG = "C:\\Users\\viper\\Desktop\\SimsMerged\\SSD_SANDBOX\\stability.log"

def log_event(msg, file=LOG_FILE):
    timestamp = time.strftime("%Y-%m-%dT%H:%M:%S")
    with open(file, "a", encoding="utf-8") as f:
        f.write(f"[{timestamp}] {msg}\n")

def check_system_health():
    """Monitors CPU and alerts if too high."""
    cpu_usage = psutil.cpu_percent(interval=0.5)
    if cpu_usage > 70:
        log_event(f"⚠️ STABILITY WARNING: High CPU Usage ({cpu_usage}%). System volatile.", STABILITY_LOG)
        return False
    return True

def run_authority():
    """Starts the Metropolis Authority as a persistent background process."""
    while not check_system_health():
        log_event("⏳ STABILITY: Waiting for CPU to cool down before launch...", STABILITY_LOG)
        time.sleep(10)

    log_event("🚀 WATCHDOG: Launching Standalone Metropolis Authority...")
    
    # Set environment variables for Git and high-frequency sync
    env = os.environ.copy()
    env["GIT_PYTHON_GIT_EXECUTABLE"] = "C:\\Users\\viper\\git\\cmd\\git.exe"
    
    # Launch uvicorn directly via subprocess.Popen (Detached)
    process = subprocess.Popen(
        [PYTHON_EXE, "-m", "uvicorn", "backend.main:app", "--host", "127.0.0.1", "--port", "8000"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        env=env,
        cwd="C:\\Users\\viper\\Desktop\\SimsMerged"
    )
    return process

if __name__ == "__main__":
    log_event("🛡️ TRIPLE WATCHDOG: Stability Layer Active. Monitoring mode only.", STABILITY_LOG)
    while True:
        # Periodic health check
        check_system_health()
        
        # Jittered sleep to reduce CPU impact
        time.sleep(15 + random.uniform(2.0, 5.0))
