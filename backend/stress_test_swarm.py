# TIMESTAMP: 2026-06-09
# PROJECT_ID: SimsMerged-v1.4.2
# AGENT_ID: viper_cli-architectssj4
# DESCRIPTION: Phase 5.1 & 5.2 - Gameplay Stress Test (50 Agents) & IOPS Throttle

import asyncio
import random
import logging
import httpx
import os
import sys
import psutil

# Ensure backend module is resolvable
sys.path.insert(0, r"C:\Users\viper\Desktop\SimsMerged")

from backend.tok_communications.tok_tree import TokTreeDAG
from backend.sprite_triplet.depin_wallet import DePINLedger
from backend.sprite_triplet.topological_wrapper import TopologicalGrid
from backend.inventory_system import InventorySystem
from backend.data_engineering.arrow_logger import TelemetryLogger

logging.basicConfig(level=logging.INFO, format='%(asctime)s | %(name)s | %(message)s')
logger = logging.getLogger("STRESS_TEST")

class SwarmStressTester:
    def __init__(self, agent_count=50):
        self.agent_count = agent_count
        self.tok_tree = TokTreeDAG()
        self.ledger = DePINLedger()
        self.grid = TopologicalGrid()
        self.inventory = InventorySystem()
        self.telemetry = TelemetryLogger()
        self.is_throttled = False
        self.base_move_delay = 0.05

    async def agent_lifecycle(self, agent_id):
        """Individual agent lifecycle: spawn -> move -> gather -> repeat."""
        # 1. Spawn & Fund
        self.grid.assign_agent_coordinate(agent_id, random.randint(0,5), random.randint(0,5))
        self.ledger.fund_wallet(agent_id, 100.0)
        
        while True:
            # 2. Pick a random target
            target = (random.randint(0, 99), random.randint(0, 99))
            
            # 3. Simulate movement (Broadcasting to GUI)
            # (Note: We skip actual A* for 50 agents in this simulation to focus on I/O stress)
            async with httpx.AsyncClient() as client:
                payload = {
                    "type": "AGENT_UPDATE",
                    "agent_id": agent_id,
                    "x": target[0],
                    "y": target[1],
                    "status": "ACTIVE"
                }
                try:
                    await client.post("http://127.0.0.1:8000/api/v1/agent/update", json=payload)
                except: pass
                
                # Step 5.2: Slow-down logic
                delay = self.base_move_delay * 2 if self.is_throttled else self.base_move_delay
                await asyncio.sleep(delay)
                
                # 4. Gather (Triggers SQL write and DePIN burn)
                await self.inventory.gather_resource(agent_id, random.choice([0, 2]))
                self.telemetry.log_event("CYCLE_COMPLETE", agent_id)

    async def monitor_performance(self):
        """Step 5.2: Monitor SSD/RAM and trigger throttle."""
        while True:
            cpu = psutil.cpu_percent()
            ram = psutil.virtual_memory().percent
            
            # Threshold: If RAM > 85% or CPU > 90%, trigger throttle
            if ram > 85 or cpu > 90:
                if not self.is_throttled:
                    logger.warning(f"!!! CRITICAL LOAD DETECTED (CPU:{cpu}%, RAM:{ram}%). Throttling Agent Ticks...")
                    self.is_throttled = True
            else:
                if self.is_throttled:
                    logger.info("Load stabilized. Resuming full speed.")
                    self.is_throttled = False
                    
            await asyncio.sleep(2)

    async def run_swarm(self):
        logger.info(f"Launching Swarm Stress Test with {self.agent_count} agents...")
        
        tasks = [asyncio.create_task(self.agent_lifecycle(f"L3_SWARM_{i:02d}")) for i in range(self.agent_count)]
        tasks.append(asyncio.create_task(self.monitor_performance()))
        
        try:
            await asyncio.gather(*tasks)
        except asyncio.CancelledError:
            pass

if __name__ == "__main__":
    tester = SwarmStressTester(agent_count=50)
    try:
        asyncio.run(tester.run_swarm())
    except KeyboardInterrupt:
        logger.info("Stress test terminated by user.")
