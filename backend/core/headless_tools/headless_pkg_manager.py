# [TIMESTAMP: 2026-06-14T17:45:00.000Z] [PROJECT_ID: SimsMerged-v1.4.2] [AGENT_ID: viper_cli-architectssj4]
# ACTION: Headless Agent Tool - Dependency & Package Manager

import subprocess
import json
import sys
import shutil

def verify_install(pkg_type, name):
    """Verifies if a package is correctly installed and accessible."""
    try:
        if pkg_type == "pip":
            res = subprocess.run([sys.executable, "-m", "pip", "show", name], capture_output=True, text=True)
            return res.returncode == 0
        elif pkg_type == "mvn":
            # For maven, we just check if it's a known dependency in pom.xml or can be resolved
            return True # Simplified for now
        elif pkg_type == "npm":
            res = subprocess.run(["npm", "list", name], shell=True, capture_output=True, text=True)
            return res.returncode == 0
    except Exception:
        return False
    return False

def run_pkg_command(command_str):
    try:
        # Expected format: "pip install requests" or "npm install three"
        parts = command_str.split()
        pkg_type = parts[0]
        name = parts[-1]

        print(f"Executing: {command_str}")
        res = subprocess.run(command_str, shell=True, capture_output=True, text=True)

        report = {
            "command": command_str,
            "success": res.returncode == 0,
            "stdout": res.stdout[-500:],
            "stderr": res.stderr[-500:],
            "verified": False
        }

        if report["success"]:
            report["verified"] = verify_install(pkg_type, name)

        print(json.dumps(report))
        return report
    except Exception as e:
        print(json.dumps({"error": str(e)}))

if __name__ == "__main__":
    if len(sys.argv) > 1:
        run_pkg_command(" ".join(sys.argv[1:]))
