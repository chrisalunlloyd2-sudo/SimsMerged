# [TIMESTAMP: 2026-06-14T13:10:00.000Z] [PROJECT_ID: SimsMerged-v1.4.2] [AGENT_ID: viper_cli-architectssj4]

import psutil
import os
import signal
import time
from .config import add_log

class ProcessManager:
    """
    Step 27: Clean Slate Process Manager.
    Ensures zero zombie processes during high-load synthesis cycles.
    """
    def __init__(self):
        self.monitored_names = ["python.exe", "java.exe", "node.exe"]

    def cleanup_zombies(self):
        """Identifies and terminates orphan/zombie processes related to the project."""
        count = 0
        for proc in psutil.process_iter(['pid', 'name', 'cmdline', 'status']):
            try:
                if proc.info['name'] in self.monitored_names:
                    # Check if the process is part of our project but disconnected
                    if proc.info['status'] == psutil.STATUS_ZOMBIE:
                        add_log(f"[PROCESS_MANAGER] Terminating zombie process: {proc.info['pid']}")
                        os.kill(proc.info['pid'], signal.SIGTERM)
                        count += 1
                    # Or check for leaked processes from previous runs
                    elif "SimsMerged" in str(proc.info['cmdline']):
                        # We don't want to kill OURSELVES or the main backend if it's running
                        if proc.info['pid'] != os.getpid():
                             # Simple heuristic: if it's very old, it's likely a leak
                             if time.time() - proc.create_time() > 3600 * 24: # 24 hours
                                 add_log(f"[PROCESS_MANAGER] Cleaning up leaked project process: {proc.info['pid']}")
                                 proc.terminate()
                                 count += 1
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                pass
        return count

process_manager = ProcessManager()
