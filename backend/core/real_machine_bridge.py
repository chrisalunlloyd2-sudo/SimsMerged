# TIMESTAMP: 2026-05-28T11:48:00.000Z
# PROJECT_ID: SimsMerged-v1.3
# AGENT_ID: Antigravity-Agent

import psutil
import time
import threading

class RealMachineBridge:
    def __init__(self):
        # Step 19: High-frequency PSUTIL binding
        self.last_stats = {
            "cpu_load": 0.0,
            "ram_load": 0.0,
            "disk_io": 0.0,
            "cpu_freq": 0.0,
            "core_usage": [],
            "timestamp": time.time()
        }
        
        self.running = True
        self.telemetry_thread = threading.Thread(target=self._telemetry_worker, daemon=True)
        self.telemetry_thread.start()

    def _telemetry_worker(self):
        """
        Background daemon thread that periodically retrieves host telemetry
        using high-performance psutil calls.
        """
        while self.running:
            try:
                # 1. CPU Load (interval=0.1 for responsiveness)
                self.last_stats["cpu_load"] = psutil.cpu_percent(interval=0.1) / 100.0
                
                # 2. RAM Distribution
                mem = psutil.virtual_memory()
                self.last_stats["ram_load"] = mem.percent / 100.0
                
                # 3. Disk I/O (Step 21 Prep)
                io = psutil.disk_io_counters()
                # We track the sum of read and write bytes
                self.last_stats["disk_io"] = (io.read_bytes + io.write_bytes)
                
                # 4. CPU Frequency
                freq = psutil.cpu_freq()
                if freq:
                    self.last_stats["cpu_freq"] = freq.current
                
                # 5. Per-Core Usage (16-core affinity mapping prep)
                self.last_stats["core_usage"] = [c / 100.0 for c in psutil.cpu_percent(percpu=True)]
                
                self.last_stats["timestamp"] = time.time()
            except Exception: pass
            time.sleep(1.0) # Update every second

    def get_actual_metrics(self):
        return self.last_stats

