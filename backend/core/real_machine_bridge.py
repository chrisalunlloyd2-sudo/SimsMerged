# TIMESTAMP: 2026-05-25T01:54:00.123Z
# PROJECT_ID: SimsMerged-v1.3
# AGENT_ID: Antigravity-Agent

import subprocess
import json
import time
import os

class RealMachineBridge:
    def __init__(self):
        self.last_stats = {}
        self.last_fetch_time = 0
        self.cache_duration = 5.0 # 5-second dynamic metrics cache for laptop safety
        
        # Static Hardware Metrics - Fetched ONCE at instantiation to save CPU cycles
        self.static_cpu = {
            "Clock": "2400 MHz",
            "Cores": 4,
            "Threads": 8
        }
        self.static_ssd = {
            "Model": "Generic NVMe SSD",
            "Firmware": "1.0.0",
            "Size": "512.0 GB"
        }
        self.static_reg = []
        
        self._init_static_hardware()

    def _init_static_hardware(self):
        """
        Gathers hardware constants once during initialization to prevent heavy WMI commands on loop.
        """
        try:
            # 1. CPU Clock and Cores
            cpu_cmd = "Get-CimInstance Win32_Processor | Select-Object -Property MaxClockSpeed, NumberOfCores, NumberOfLogicalProcessors | ConvertTo-Json"
            cpu_raw = subprocess.check_output(["powershell", "-Command", cpu_cmd], timeout=5).decode('utf-8')
            cpu_data = json.loads(cpu_raw)
            if isinstance(cpu_data, list): cpu_data = cpu_data[0]
            
            self.static_cpu = {
                "Clock": f"{cpu_data.get('MaxClockSpeed', 2400)} MHz",
                "Cores": cpu_data.get('NumberOfCores', 4),
                "Threads": cpu_data.get('NumberOfLogicalProcessors', 8)
            }
            
            # 2. SSD Specifications
            disk_cmd = "Get-CimInstance Win32_DiskDrive | Select-Object -Property Model, FirmwareRevision, Size | ConvertTo-Json"
            disk_raw = subprocess.check_output(["powershell", "-Command", disk_cmd], timeout=5).decode('utf-8')
            disk_data = json.loads(disk_raw)
            if isinstance(disk_data, list): disk_data = disk_data[0]
            
            size_gb = int(disk_data.get('Size', 512 * 1024 * 1024 * 1024)) / 1024 / 1024 / 1024
            self.static_ssd = {
                "Model": disk_data.get('Model', 'Generic NVMe SSD').strip(),
                "Firmware": disk_data.get('FirmwareRevision', 'Unknown').strip(),
                "Size": f"{size_gb:.1f} GB"
            }
            
            # 3. Registry Sample list
            reg_cmd = 'Get-ChildItem "HKLM:\\SOFTWARE" | Select-Object -First 10 -Property Name | ConvertTo-Json'
            reg_raw = subprocess.check_output(["powershell", "-Command", reg_cmd], timeout=5).decode('utf-8')
            self.static_reg = json.loads(reg_raw)
            
        except Exception:
            # Fallback nominal values in case of permission issues
            self.static_reg = [{"Name": "HKEY_LOCAL_MACHINE\\SOFTWARE\\Nominal"}]

    def get_actual_metrics(self):
        """
        Fetches dynamic metrics (CPU load, free memory, active processes) in a single unified PowerShell call.
        Uses a 5-second cache to prevent laptop slowdowns.
        """
        now = time.time()
        if self.last_stats and (now - self.last_fetch_time < self.cache_duration):
            return self.last_stats
            
        try:
            # Unified powershell command to get both CPU percent, OS Memory, and Top Processes in a single shell spawn
            unified_cmd = (
                "$cpu = (Get-CimInstance Win32_Processor | Select-Object -Property LoadPercentage).LoadPercentage; "
                "$os = Get-CimInstance Win32_OperatingSystem | Select-Object -Property FreePhysicalMemory, TotalVisibleMemorySize, TotalVirtualMemorySize, FreeVirtualMemory; "
                "$procs = Get-Process | Select-Object -Property Name, Id, CPU, WorkingSet | Sort-Object CPU -Descending | Select-Object -First 12 | ConvertTo-Json; "
                "@{cpu=$cpu; free_phys=$os.FreePhysicalMemory; total_phys=$os.TotalVisibleMemorySize; free_virt=$os.FreeVirtualMemory; total_virt=$os.TotalVirtualMemorySize; procs=$procs} | ConvertTo-Json"
            )
            
            raw_out = subprocess.check_output(["powershell", "-Command", unified_cmd], timeout=8).decode('utf-8')
            payload = json.loads(raw_out)
            
            # Parse processes
            procs_payload = payload.get("procs", "[]")
            proc_list = json.loads(procs_payload) if isinstance(procs_payload, str) else procs_payload
            if isinstance(proc_list, dict):
                proc_list = [proc_list]
                
            # Parse memory
            total_phys = float(payload.get("total_phys", 8 * 1024 * 1024))
            free_phys = float(payload.get("free_phys", 4 * 1024 * 1024))
            used_phys = total_phys - free_phys
            
            total_virt = float(payload.get("total_virt", 16 * 1024 * 1024))
            free_virt = float(payload.get("free_virt", 8 * 1024 * 1024))
            used_virt = total_virt - free_virt
            
            cpu_pct = float(payload.get("cpu", 10))
            
            self.last_stats = {
                "CPU": {
                    "Load": f"{cpu_pct:.0f}%",
                    "Clock": self.static_cpu["Clock"],
                    "Cores": self.static_cpu["Cores"],
                    "Threads": self.static_cpu["Threads"]
                },
                "RAM": {
                    "Physical_Used": f"{(used_phys / total_phys * 100):.1f}%",
                    "Virtual_Used": f"{(used_virt / total_virt * 100):.1f}%",
                    "Commit_Total_GB": f"{(total_virt / 1024 / 1024):.1f} GB"
                },
                "REGISTRY_SAMPLE": self.static_reg,
                "SSD": self.static_ssd,
                "processes": proc_list,
                "real_cpu_load": cpu_pct / 100.0,
                "real_mem_pct": used_phys / total_phys,
                "real_virt_pct": used_virt / total_virt,
                "real_cpu_mhz": float(self.static_cpu["Clock"].split()[0]),
                "real_mem_total_kb": total_phys,
                "timestamp": now
            }
            self.last_fetch_time = now
            return self.last_stats
            
        except Exception as e:
            # Fallback to last cached metrics to guarantee non-blocking API behavior if host times out
            if self.last_stats:
                return self.last_stats
            return {"error": str(e)}
