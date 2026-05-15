import asyncio
import time
import json
from .agent_registrar import update_agents

async def start_orchestrator():
    print("Orchestrator online. Managing agent life cycles.")
    while True:
        update_agents()
        with open("../PULSE_HEARTBEAT.txt", "w") as f:
            f.write(str(time.time()))
        await asyncio.sleep(1.2) # 1.2s Sync Protocol