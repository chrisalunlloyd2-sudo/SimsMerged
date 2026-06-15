# TIMESTAMP: 2026-06-09
# PROJECT_ID: SimsMerged-v1.4.2
# AGENT_ID: viper_cli-architectssj4
# DESCRIPTION: Phase 3.3 - Agent Movement & Gathering Simulation

import json
import time
import httpx
import asyncio
import sys
import os

sys.path.insert(0, r"C:\Users\viper\Desktop\SimsMerged")
from backend.pathfinder import AStarPathfinder
from backend.inventory_system import InventorySystem

async def simulate_agent_lifecycle(agent_id, start_pos, target_pos):
    # 1. Load Map
    map_path = r"C:\Users\viper\Desktop\SimsMerged\backend\world_map.json"
    with open(map_path, 'r') as f:
        world_data = json.load(f)
    
    matrix = world_data['matrix']
    inv_sys = InventorySystem()
    
    # 2. Pathfinding
    pathfinder = AStarPathfinder(matrix)
    print(f"[SIM] Calculating path for {agent_id} from {start_pos} to {target_pos}...")
    path = pathfinder.find_path(start_pos, target_pos)
    
    if not path:
        print("[SIM] No path found!")
        return

    # 3. Step through path
    async with httpx.AsyncClient() as client:
        for step in path:
            x, y = step
            payload = {
                "type": "AGENT_UPDATE",
                "agent_id": agent_id,
                "x": x,
                "y": y,
                "status": "ACTIVE"
            }
            await client.post("http://127.0.0.1:8000/api/v1/agent/update", json=payload)
            await asyncio.sleep(0.05)

        # 4. Gather Resource at target
        terrain = matrix[target_pos[0]][target_pos[1]]
        print(f"[SIM] Agent {agent_id} reached target {target_pos}. Initiating gathering...")
        
        success = await inv_sys.gather_resource(agent_id, terrain)
        
        if success:
            # 5. Broadcast inventory update to GUI
            inventory = inv_sys.get_inventory(agent_id)
            inv_dict = {item[0]: item[1] for item in inventory}
            
            payload = {
                "type": "AGENT_UPDATE",
                "agent_id": agent_id,
                "x": target_pos[0],
                "y": target_pos[1],
                "status": "ACTIVE",
                "inventory": inv_dict
            }
            await client.post("http://127.0.0.1:8000/api/v1/agent/update", json=payload)
            print(f"[SIM] Inventory updated: {inv_dict}")

if __name__ == "__main__":
    agent = "L3_PIONEER_01"
    start = (0, 0)
    target = (5, 5) # Assuming (5,5) is Grass or Stone
    asyncio.run(simulate_agent_lifecycle(agent, start, target))
