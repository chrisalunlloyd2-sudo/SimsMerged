# TIMESTAMP: 2026-06-09
# PROJECT_ID: SimsMerged-v1.4.2
# AGENT_ID: viper_cli-architectssj4
# DESCRIPTION: Phase 2.3 - Agent Movement Simulation with A* and WebSockets

import json
import time
import httpx
import asyncio
import sys
import os

sys.path.insert(0, r"C:\Users\viper\Desktop\SimsMerged")
from backend.pathfinder import AStarPathfinder

async def simulate_agent_movement(agent_id, start_pos, target_pos):
    # 1. Load Map
    map_path = r"C:\Users\viper\Desktop\SimsMerged\backend\world_map.json"
    with open(map_path, 'r') as f:
        world_data = json.load(f)

    matrix = world_data['matrix']

    # 2. Pathfinding
    pathfinder = AStarPathfinder(matrix)
    print(f"[SIM] Calculating path for {agent_id} from {start_pos} to {target_pos}...")
    path = pathfinder.find_path(start_pos, target_pos)

    if not path:
        print("[SIM] No path found!")
        return

    print(f"[SIM] Path found: {len(path)} steps.")

    # 3. Step through path and broadcast to WebSocket
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
            try:
                await client.post("http://127.0.0.1:8000/api/v1/agent/update", json=payload)
            except Exception as e:
                print(f"[SIM] Failed to send update: {e}")

            # Simulated move time
            await asyncio.sleep(0.1) # 100ms per tile for smooth-ish visual

    print(f"[SIM] Agent {agent_id} reached target {target_pos}.")

if __name__ == "__main__":
    agent = "L3_PIONEER_01"
    start = (0, 0)
    target = (15, 15)
    asyncio.run(simulate_agent_movement(agent, start, target))
