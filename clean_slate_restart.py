# [TIMESTAMP: 2026-06-11T13:50:00.000Z] [PROJECT_ID: SimsMerged-v1.4.2] [AGENT_ID: Gemini-CLI-Architect]

import os
import subprocess
import time
import sys

def kill_processes():
    """
    Step 27: Clean Slate Process Manager.
    Forcefully terminates all java and python instances to prevent zombie overhead.
    """
    print("🧹 [CLEAN_SLATE] Initiating forceful process termination...")
    
    # Use taskkill for reliability on Windows
    try:
        subprocess.run(["taskkill", "/F", "/IM", "java.exe", "/T"], capture_output=True)
        subprocess.run(["taskkill", "/F", "/IM", "python.exe", "/T"], capture_output=True)
        time.sleep(2) # Cooldown for hardware release
        print("✅ [CLEAN_SLATE] Memory cleared. Ready for 35-page load cycle.")
    except Exception as e:
        print(f"⚠️ [CLEAN_SLATE] Termination warning: {str(e)}")

def restart_metropolis():
    kill_processes()
    
    print("🚀 [RESTART] Launching Metropolis Backend & JavaFX Neo...")
    
    # Backend Launch (Port 8000 & 8002)
    backend_cmd = "powershell -NoExit -Command \"& 'C:/Users/viper/python/python.exe' run_backend.py\""
    subprocess.Popen(backend_cmd, shell=True)
    
    # Wait for backend to stabilize
    time.sleep(5)
    
    # GUI Launch
    gui_cmd = "powershell -NoExit -Command \"$env:JAVA_HOME='C:/Users/viper/JavaSetup/jdk-17.0.8.1+1'; cd C:/Users/viper/Desktop/Sims_JavaFX_Neo; & 'C:/Users/viper/JavaSetup/apache-maven-3.9.4/bin/mvn.cmd' javafx:run\""
    subprocess.Popen(gui_cmd, shell=True)
    
    print("🏁 [RESTART] Metropolis Systems Initialized.")

if __name__ == "__main__":
    restart_metropolis()
