# [TIMESTAMP: 2026-06-05T01:10:00.000Z] [PROJECT_ID: SimsMerged-v1.4] [AGENT_ID: Antigravity-CLI-Architect]

import os
import time
import subprocess
import sys

def check_process_running(process_name):
    try:
        output = subprocess.check_output('tasklist', shell=True).decode()
        return process_name.lower() in output.lower()
    except Exception:
        return False

def main():
    print("[WATCHDOG_A] Starting persistence monitor...")
    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
    backend_script = os.path.join(project_root, "run_backend.py")
    powershell_watchdog = os.path.join(project_root, "build_scripts", "watchdog_b.ps1")

    while True:
        # 1. Check Backend
        if not check_process_running("python.exe") or not check_process_running("uvicorn"):
            print("[WATCHDOG_A] Backend offline! Restarting...")
            subprocess.Popen([sys.executable, backend_script], cwd=project_root)

        # 2. Check Watchdog B (PowerShell)
        # We can check for powershell processes running the specific script
        try:
            output = subprocess.check_output('powershell -Command "Get-Process | Where-Object {$_.CommandLine -like \'*watchdog_b.ps1*\'}"', shell=True).decode()
            if not output.strip():
                print("[WATCHDOG_A] Watchdog B offline! Restarting...")
                subprocess.Popen(["powershell", "-File", powershell_watchdog], cwd=project_root)
        except Exception:
            pass

        time.sleep(30)

if __name__ == "__main__":
    main()
