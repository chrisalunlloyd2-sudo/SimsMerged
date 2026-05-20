import subprocess
import json
import time

class RealMachineBridge:
    def __init__(self):
        self.last_stats = {}

    def get_actual_metrics(self):
        """
        Executes PowerShell commands to fetch REAL host machine telemetry.
        """
        try:
            # 1. Fetch CPU Load and Clock
            cpu_cmd = "Get-CimInstance Win32_Processor | Select-Object -Property LoadPercentage, MaxClockSpeed | ConvertTo-Json"
            cpu_raw = subprocess.check_output(["powershell", "-Command", cpu_cmd], stderr=subprocess.STDOUT).decode('utf-8')
            cpu_data = json.loads(cpu_raw)
            
            # 2. Fetch RAM usage
            mem_cmd = "Get-CimInstance Win32_OperatingSystem | Select-Object -Property FreePhysicalMemory, TotalVisibleMemorySize | ConvertTo-Json"
            mem_raw = subprocess.check_output(["powershell", "-Command", mem_cmd], stderr=subprocess.STDOUT).decode('utf-8')
            mem_data = json.loads(mem_raw)
            
            # Normalize to 0-1 range
            load = cpu_data.get("LoadPercentage", 0) / 100.0
            total_mem = mem_data.get("TotalVisibleMemorySize", 1)
            used_mem = total_mem - mem_data.get("FreePhysicalMemory", 0)
            mem_pct = used_mem / total_mem
            
            self.last_stats = {
                "real_cpu_load": float(load),
                "real_cpu_mhz": int(cpu_data.get("MaxClockSpeed", 0)),
                "real_mem_pct": float(mem_pct),
                "real_mem_total_kb": int(total_mem),
                "timestamp": time.time()
            }
            return self.last_stats
        except Exception as e:
            print(f"TELEMETRY_ERROR: {e}")
            return {"error": str(e)}

if __name__ == "__main__":
    bridge = RealMachineBridge()
    print(json.dumps(bridge.get_actual_metrics(), indent=2))
