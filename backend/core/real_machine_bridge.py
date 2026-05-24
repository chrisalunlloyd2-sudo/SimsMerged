import subprocess
import json
import time
import os

class RealMachineBridge:
    def __init__(self):
        self.last_stats = {}
        self.last_fetch_time = 0
        self.cache_duration = 2.0 # 2.0 second telemetry cache

    def get_actual_metrics(self):
        """
        Executes exhaustive PowerShell commands to fetch REAL host machine telemetry with a 2-second cache.
        """
        now = time.time()
        if self.last_stats and (now - self.last_fetch_time < self.cache_duration):
            return self.last_stats
        try:
            # 1. CPU: Exhaustive
            cpu_cmd = "Get-CimInstance Win32_Processor | Select-Object -Property LoadPercentage, MaxClockSpeed, L2CacheSize, L3CacheSize, NumberOfCores, NumberOfLogicalProcessors | ConvertTo-Json"
            cpu_raw = subprocess.check_output(["powershell", "-Command", cpu_cmd]).decode('utf-8')
            cpu_data = json.loads(cpu_raw)
            if isinstance(cpu_data, list): cpu_data = cpu_data[0]

            # 2. RAM & VMM: Real physical and committed memory (Step 42 Option A)
            mem_cmd = "Get-CimInstance Win32_OperatingSystem | Select-Object -Property FreePhysicalMemory, TotalVisibleMemorySize, TotalVirtualMemorySize, FreeVirtualMemory | ConvertTo-Json"
            mem_raw = subprocess.check_output(["powershell", "-Command", mem_cmd]).decode('utf-8')
            mem_data = json.loads(mem_raw)
            
            # 3. Registry Sample (Step 42 Option B)
            reg_cmd = 'Get-ChildItem "HKLM:\\SOFTWARE" | Select-Object -First 20 -Property Name | ConvertTo-Json'
            reg_raw = subprocess.check_output(["powershell", "-Command", reg_cmd]).decode('utf-8')
            reg_keys = json.loads(reg_raw)

            # 4. SSD: Exhaustive
            disk_cmd = "Get-CimInstance Win32_DiskDrive | Select-Object -Property Model, FirmwareRevision, Size, InterfaceType | ConvertTo-Json"
            disk_raw = subprocess.check_output(["powershell", "-Command", disk_cmd]).decode('utf-8')
            disk_data = json.loads(disk_raw)
            if isinstance(disk_data, list): disk_data = disk_data[0]

            # 5. Process Mapping
            proc_cmd = "Get-Process | Select-Object -Property Name, Id, CPU, WorkingSet | Sort-Object CPU -Descending | Select-Object -First 15 | ConvertTo-Json"
            proc_raw = subprocess.check_output(["powershell", "-Command", proc_cmd]).decode('utf-8')
            proc_list = json.loads(proc_raw)
            
            total_phys = mem_data.get("TotalVisibleMemorySize", 1)
            used_phys = total_phys - mem_data.get("FreePhysicalMemory", 0)
            
            total_virt = mem_data.get("TotalVirtualMemorySize", 1)
            used_virt = total_virt - mem_data.get("FreeVirtualMemory", 0)
            
            self.last_stats = {
                "CPU": {
                    "Load": f"{cpu_data.get('LoadPercentage', 0)}%",
                    "Clock": f"{cpu_data.get('MaxClockSpeed', 0)} MHz",
                    "Cores": cpu_data.get('NumberOfCores', 0),
                    "Threads": cpu_data.get('NumberOfLogicalProcessors', 0)
                },
                "RAM": {
                    "Physical_Used": f"{(used_phys / total_phys * 100):.1f}%",
                    "Virtual_Used": f"{(used_virt / total_virt * 100):.1f}%",
                    "Commit_Total_GB": f"{(total_virt / 1024 / 1024):.1f} GB"
                },
                "REGISTRY_SAMPLE": reg_keys,
                "SSD": {
                    "Model": disk_data.get('Model', 'Unknown'),
                    "Firmware": disk_data.get('FirmwareRevision', 'Unknown'),
                    "Size": f"{(int(disk_data.get('Size', 0)) / 1024 / 1024 / 1024):.1f} GB"
                },
                "processes": proc_list,
                "real_cpu_load": cpu_data.get('LoadPercentage', 0) / 100.0,
                "real_mem_pct": used_phys / total_phys,
                "real_virt_pct": used_virt / total_virt,
                "real_cpu_mhz": cpu_data.get('MaxClockSpeed', 0),
                "real_mem_total_kb": total_phys,
                "timestamp": time.time()
            }
            self.last_fetch_time = now
            return self.last_stats
        except Exception as e:
            return {"error": str(e)}

if __name__ == "__main__":
    bridge = RealMachineBridge()
    print(json.dumps(bridge.get_actual_metrics(), indent=2))
