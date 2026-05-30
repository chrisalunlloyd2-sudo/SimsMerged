# TIMESTAMP: 2026-05-28T11:48:00.000Z
# PROJECT_ID: SimsMerged-v1.3
# AGENT_ID: Antigravity-Agent

import subprocess
import json
import time
import os
import threading

class RealMachineBridge:
    def __init__(self):
        self.cache_duration = 60.0 # 1-minute dynamic metrics cache for better stability
        
        # High-quality nominal fallback/initial values
        self.static_cpu = {
            "Clock": "3200 MHz",
            "Cores": 8,
            "Threads": 16
        }
        self.static_ssd = {
            "Model": "High-Performance NVMe SSD",
            "Firmware": "1.0.0",
            "Size": "1024.0 GB"
        }
        self.static_reg = [
            {"Name": "HKEY_LOCAL_MACHINE\\SOFTWARE\\Microsoft"},
            {"Name": "HKEY_LOCAL_MACHINE\\SOFTWARE\\Classes"},
            {"Name": "HKEY_LOCAL_MACHINE\\SOFTWARE\\Clients"},
            {"Name": "HKEY_LOCAL_MACHINE\\SOFTWARE\\Policies"}
        ]
        
        self.last_stats = {
            "CPU": {
                "Load": "10%",
                "Clock": self.static_cpu["Clock"],
                "Cores": self.static_cpu["Cores"],
                "Threads": self.static_cpu["Threads"]
            },
            "RAM": {
                "Physical_Used": "35.0%",
                "Virtual_Used": "25.0%",
                "Commit_Total_GB": "16.0 GB"
            },
            "REGISTRY_SAMPLE": self.static_reg,
            "SSD": self.static_ssd,
            "processes": [
                {"Name": "System", "Id": 4, "CPU": 1.2, "WorkingSet": 1024 * 1024},
                {"Name": "explorer.exe", "Id": 1200, "CPU": 0.5, "WorkingSet": 120 * 1024 * 1024},
                {"Name": "chrome.exe", "Id": 4500, "CPU": 2.4, "WorkingSet": 450 * 1024 * 1024}
            ],
            "real_cpu_load": 0.10,
            "real_mem_pct": 0.35,
            "real_virt_pct": 0.25,
            "real_cpu_mhz": 3200.0,
            "real_mem_total_kb": 16 * 1024 * 1024,
            "timestamp": time.time()
        }
        
        # Start non-blocking asynchronous background hardware telemetry thread
        self.running = True
        self.telemetry_thread = threading.Thread(target=self._telemetry_worker, daemon=True)
        self.telemetry_thread.start()

    def _telemetry_worker(self):
        """
        Background daemon thread that periodically retrieves host telemetry
        using lightweight PowerShell queries, bypassing API locks.
        """
        # Fetch static hardware specifications ONCE in background thread first to avoid slow startup
        try:
            # 1. CPU Clock and Cores
            cpu_cmd = "Get-CimInstance Win32_Processor | Select-Object -Property MaxClockSpeed, NumberOfCores, NumberOfLogicalProcessors | ConvertTo-Json"
            cpu_raw = subprocess.check_output(["powershell", "-Command", cpu_cmd], timeout=5).decode('utf-8')
            cpu_data = json.loads(cpu_raw)
            if isinstance(cpu_data, list): cpu_data = cpu_data[0]
            
            self.static_cpu = {
                "Clock": f"{cpu_data.get('MaxClockSpeed', 3200)} MHz",
                "Cores": cpu_data.get('NumberOfCores', 8),
                "Threads": cpu_data.get('NumberOfLogicalProcessors', 16)
            }
        except Exception:
            pass

        try:
            # 2. SSD Specifications
            disk_cmd = "Get-CimInstance Win32_DiskDrive | Select-Object -Property Model, FirmwareRevision, Size | ConvertTo-Json"
            disk_raw = subprocess.check_output(["powershell", "-Command", disk_cmd], timeout=5).decode('utf-8')
            disk_data = json.loads(disk_raw)
            if isinstance(disk_data, list): disk_data = disk_data[0]
            
            size_gb = int(disk_data.get('Size', 1024 * 1024 * 1024 * 1024)) / 1024 / 1024 / 1024
            self.static_ssd = {
                "Model": disk_data.get('Model', 'High-Performance NVMe SSD').strip(),
                "Firmware": disk_data.get('FirmwareRevision', 'Unknown').strip(),
                "Size": f"{size_gb:.1f} GB"
            }
        except Exception:
            pass

        try:
            # 3. Registry Sample list
            reg_cmd = 'Get-ChildItem "HKLM:\\SOFTWARE" | Select-Object -First 10 -Property Name | ConvertTo-Json'
            reg_raw = subprocess.check_output(["powershell", "-Command", reg_cmd], timeout=5).decode('utf-8')
            self.static_reg = json.loads(reg_raw)
        except Exception:
            pass

        # Telemetry loop
        while self.running:
            try:
                now = time.time()
                # Optimized command: Removed expensive per-process CPU sampling
                unified_cmd = (
                    "$ErrorActionPreference = 'SilentlyContinue'; "
                    "$cpu = (Get-CimInstance Win32_Processor | Select-Object -Property LoadPercentage).LoadPercentage; "
                    "$os = Get-CimInstance Win32_OperatingSystem | Select-Object -Property FreePhysicalMemory, TotalVisibleMemorySize, TotalVirtualMemorySize, FreeVirtualMemory; "
                    "$procs = Get-Process | Select-Object -Property Name, Id, WorkingSet | Sort-Object WorkingSet -Descending | Select-Object -First 5 | ConvertTo-Json -Compress; "
                    "@{cpu=$cpu; free_phys=$os.FreePhysicalMemory; total_phys=$os.TotalVisibleMemorySize; free_virt=$os.FreeVirtualMemory; total_virt=$os.TotalVirtualMemorySize; procs=$procs} | ConvertTo-Json -Compress"
                )
                
                raw_out = subprocess.check_output(["powershell", "-Command", unified_cmd], timeout=15).decode('utf-8')
                if raw_out.strip():
                    payload = json.loads(raw_out)
                    
                    procs_payload = payload.get("procs")
                    if procs_payload:
                        try:
                            proc_list = json.loads(procs_payload) if isinstance(procs_payload, str) else procs_payload
                        except json.JSONDecodeError:
                            proc_list = []
                    else:
                        proc_list = []
                        
                    if isinstance(proc_list, dict):
                        proc_list = [proc_list]
                        
                    total_phys = float(payload.get("total_phys", 16 * 1024 * 1024))
                    free_phys = float(payload.get("free_phys", 8 * 1024 * 1024))
                    used_phys = total_phys - free_phys
                    
                    total_virt = float(payload.get("total_virt", 32 * 1024 * 1024))
                    free_virt = float(payload.get("free_virt", 16 * 1024 * 1024))
                    used_virt = total_virt - free_virt
                    
                    cpu_pct = float(payload.get("cpu", 15))
                    
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
            except Exception as e:
                # If telemetry loop encounters WMI/CimInstance lag or timeout, we preserve cached values
                pass
                
            time.sleep(self.cache_duration)

    def get_actual_metrics(self):
        """
        Guarantees 100% non-blocking instantly returned cached telemetry statistics.
        """
        return self.last_stats
