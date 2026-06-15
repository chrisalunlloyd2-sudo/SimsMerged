# TIMESTAMP: 2026-06-09
# PROJECT_ID: SimsMerged-v1.4.2
# AGENT_ID: viper_cli-architectssj4
# DESCRIPTION: Phase 6 - Apache Arrow High-Speed Telemetry Logger

import pyarrow as pa
import pyarrow.parquet as pq
import time
import os
import psutil
import logging
from datetime import datetime
from typing import Dict, Any

logger = logging.getLogger("ArrowLogger")
logger.setLevel(logging.INFO)

class TelemetryLogger:
    def __init__(self, log_dir: str = r"C:\Users\viper\Desktop\SimsMerged\backend\telemetry"):
        self.log_dir = log_dir
        if not os.path.exists(self.log_dir):
            os.makedirs(self.log_dir, exist_ok=True)
            
        # Step 60: Finalize logging schemas
        self.schema = pa.schema([
            ('timestamp', pa.float64()),
            ('event_type', pa.string()),
            ('agent_id', pa.string()),
            ('cpu_percent', pa.float32()),
            ('ram_mb', pa.float32()),
            ('ssd_read_bytes', pa.int64()),
            ('ssd_write_bytes', pa.int64()),
            ('payload_json', pa.string()) # JSON string for flexible data
        ])
        
        self.batch_data = {
            'timestamp': [], 'event_type': [], 'agent_id': [],
            'cpu_percent': [], 'ram_mb': [], 'ssd_read_bytes': [],
            'ssd_write_bytes': [], 'payload_json': []
        }
        self.batch_size = 100 # Flush to disk after 100 events

    def log_event(self, event_type: str, agent_id: str, payload_json: str = "{}"):
        """Step 51: High-speed appending of telemetry data."""
        # Step 58: Monitor SSD IOPS vs RAM metrics
        process = psutil.Process(os.getpid())
        io_counters = psutil.disk_io_counters()
        
        self.batch_data['timestamp'].append(time.time())
        self.batch_data['event_type'].append(event_type)
        self.batch_data['agent_id'].append(agent_id)
        self.batch_data['cpu_percent'].append(psutil.cpu_percent(interval=None))
        self.batch_data['ram_mb'].append(process.memory_info().rss / (1024 * 1024))
        
        # Guard against None io_counters
        read_bytes = io_counters.read_bytes if io_counters else 0
        write_bytes = io_counters.write_bytes if io_counters else 0
        self.batch_data['ssd_read_bytes'].append(read_bytes)
        self.batch_data['ssd_write_bytes'].append(write_bytes)
        self.batch_data['payload_json'].append(payload_json)
        
        if len(self.batch_data['timestamp']) >= self.batch_size:
            self.flush_to_parquet()

    def flush_to_parquet(self):
        """Flushes the current batch to a columnar Parquet file using Apache Arrow."""
        if not self.batch_data['timestamp']:
            return
            
        table = pa.Table.from_pydict(self.batch_data, schema=self.schema)
        filename = f"telemetry_{datetime.now().strftime('%Y%m%d_%H%M%S')}.parquet"
        filepath = os.path.join(self.log_dir, filename)
        
        pq.write_table(table, filepath)
        logger.info(f"Flushed {len(self.batch_data['timestamp'])} events to {filename}")
        
        # Reset batch
        for key in self.batch_data:
            self.batch_data[key] = []

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    t_logger = TelemetryLogger()
    
    # Simulate high speed logging
    logger.info("Simulating high-speed Arrow logging...")
    for i in range(105): # Over 100 to trigger a flush
        t_logger.log_event("TEST_EVENT", "L3_MINER", '{"task": "mining"}')
        
    logger.info("Done.")
