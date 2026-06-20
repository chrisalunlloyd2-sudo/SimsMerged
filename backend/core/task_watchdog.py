# [TIMESTAMP: 2026-06-08T05:30:00.000Z] [PROJECT_ID: SimsMerged-v1.4.2] [AGENT_ID: viper_cli-architectssj4]

import asyncio
import time
import os
from .config import SYSLOG_PATH, add_log, add_message

class TaskWatchdog:
    """
    TASK WATCHDOG:
    - Monitors backend loops and SLM request latency.
    - Clears hung queues if physical I/O limits are exceeded.
    - Ensures the Metropolis is 'Always Advancing'.
    """
    def __init__(self, model_orchestrator):
        self.orchestrator = model_orchestrator
        self.last_queue_size = 0
        self.stuck_counter = 0

    async def run_watchdog_loop(self):
        add_log("[WATCHDOG] Performance Monitor Active.")
        while True:
            await asyncio.sleep(30)
            current_queue = len(self.orchestrator.queue)

            # Detect queue stagnation (Hung physical SSD access)
            if current_queue > 0 and current_queue == self.last_queue_size:
                self.stuck_counter += 1
            else:
                self.stuck_counter = 0

            if self.stuck_counter >= 4: # Stuck for 2 minutes
                add_log(f"[WATCHDOG] Detect neural hang. Queue size: {current_queue}. CLEARING...", "warning")
                add_message("System_Watchdog", "⚠️ NEURAL_HANG detected due to physical I/O limits. Flushing queue to restore grid stability.")
                while self.orchestrator.queue:
                    task = self.orchestrator.queue.popleft()
                    if not task["future"].done():
                        task["future"].set_result("[SSD_I/O_FLUSH] Weights dropped to prevent host lag.")
                self.stuck_counter = 0

            self.last_queue_size = current_queue

async def start_watchdog_task(model_orchestrator):
    watchdog = TaskWatchdog(model_orchestrator)
    await watchdog.run_watchdog_loop()
