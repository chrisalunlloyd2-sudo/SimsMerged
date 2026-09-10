# TIMESTAMP: 2026-06-09
# PROJECT_ID: SimsMerged-v1.4.2
# AGENT_ID: viper_cli-architectssj4
# DESCRIPTION: Updated MSN Metropolis with Social Sandbox & 4-Turn Loop Breaker

from fastapi import FastAPI, WebSocket, WebSocketDisconnect, HTTPException
from pydantic import BaseModel
import sqlite3
import uvicorn
import time
import json
import logging
import random
from typing import List, Dict, Any
import os
import sys

# Ensure backend module is resolvable
sys.path.insert(0, r"C:\Users\viper\Desktop\SimsMerged")

from backend.sprite_triplet.depin_wallet import DePINLedger
from backend.tok_communications.tok_tree import TokTreeDAG

logger = logging.getLogger("MSN_Metropolis")
logger.setLevel(logging.INFO)

app = FastAPI(title="MSN Metropolis Chat API", version="1.0")

# Persistent state
ledger = DePINLedger()
tok_tree = TokTreeDAG()

# Step 8.4: Loop Breaker State
CONSECUTIVE_AGENT_TURNS = 0
MAX_AGENT_TURNS = 4

# Phase 8: Social State
PERSONA_PATH = os.path.join(r"C:\Users\viper\Desktop\SimsMerged\backend", "personas.json")
with open(PERSONA_PATH, "r") as f:
    persona_data = json.load(f)["personas"]

class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        if websocket in self.active_connections:
            self.active_connections.remove(websocket)

    async def broadcast(self, message: str):
        for connection in self.active_connections:
            try:
                await connection.send_text(message)
            except Exception as e:
                logger.error(f"Failed to send message: {e}")

import psutil
import asyncio

manager = ConnectionManager()

# HYPER-EXPANSION: Hardware Telemetry Loop
async def hardware_telemetry_loop():
    """Broadcasts real-machine hardware telemetry to the JavaFX HUD."""
    while True:
        try:
            cpu = psutil.cpu_percent(interval=1)
            disk = psutil.disk_io_counters()
            # IO Stress heuristic (Normalized)
            io_total = (disk.read_bytes + disk.write_bytes) / (1024 * 1024)
            io_stress = min(100, io_total / 50.0 * 100)

            telemetry = {
                "type": "TELEMETRY_UPDATE",
                "cpu": cpu,
                "io": io_stress
            }
            await manager.broadcast(json.dumps(telemetry))
        except Exception as e:
            logger.error(f"Telemetry Error: {e}")
        await asyncio.sleep(2)

@app.on_event("startup")
async def startup_event():
    asyncio.create_task(hardware_telemetry_loop())

@app.websocket("/ws/chat/{client_id}")
async def websocket_endpoint(websocket: WebSocket, client_id: str):
    global CONSECUTIVE_AGENT_TURNS
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()

            if client_id == "GodHandUI":
                # Human reset
                CONSECUTIVE_AGENT_TURNS = 0
                if data.startswith("/"):
                    await process_slash_command(client_id, data)
                else:
                    await manager.broadcast(f"Viper: {data}")
            else:
                # Agent turn
                CONSECUTIVE_AGENT_TURNS += 1
                if CONSECUTIVE_AGENT_TURNS > MAX_AGENT_TURNS:
                    await manager.broadcast("[System] 4-Turn Loop Breaker Active. Agents forced to IDLE.")
                    CONSECUTIVE_AGENT_TURNS = 0 # Reset after breaking
                    continue
                await manager.broadcast(f"{client_id}: {data}")

    except WebSocketDisconnect:
        manager.disconnect(websocket)

async def process_slash_command(client_id: str, command: str):
    parts = command.split()
    cmd_type = parts[0].lower()

    if cmd_type == "/fund":
        if len(parts) >= 3:
            agent_id, amount = parts[1], float(parts[2])
            ledger.fund_wallet(agent_id, amount)
            persona = persona_data[0]
            status_msg = f"{persona['base_status']} | Funded: {amount} tokens"
            await manager.broadcast(json.dumps({"type": "AGENT_UPDATE", "agent_id": agent_id, "status": status_msg}))
            await manager.broadcast(f"[God Hand] Funded {amount} to {agent_id}")

    elif cmd_type == "/assign":
        if len(parts) >= 3:
            agent_id, task_name = parts[1], " ".join(parts[2:])
            await manager.broadcast(f"[God Hand] Assigning '{task_name}' to {agent_id}...")

            # PHASE 25: Sovereign Intervention - Update agent internal DAG
            from backend.core.config import METROPOLIS_AGENTS
            agent = next((a for a in METROPOLIS_AGENTS if a["id"] == agent_id or a["name"] == agent_id), None)
            if agent:
                agent["last_action"] = "Sovereign_Task"
                agent["chain_of_thought"] = f"Assigned by God Hand: {task_name}"
                agent["status"] = "GATHERING" if "Gather" in task_name else ("DELIVERING" if "Build" in task_name else "WORKING")

                # Push task to actions agent for synthesis
                from backend.core.action_agent import actions_agent
                import asyncio

                async def execute_sovereign_task():
                    try:
                        await actions_agent.synthesize_recursive(f"Execute Sovereign Mandate: {task_name}", "python")
                        await manager.broadcast(f"{agent_id}: (u) Task '{task_name}' synthesis complete. Awaiting physical deployment.")
                        agent["status"] = "ACTIVE"
                        agent["chain_of_thought"] = "Sovereign Task Complete. Returning to autonomous loop."

                        # Trigger structural update
                        await manager.broadcast(json.dumps({"type": "AGENT_UPDATE", "agent_id": agent_id, "status": agent["status"]}))
                    except Exception as e:
                        logger.error(f"Sovereign task execution failed: {e}")
                        await manager.broadcast(f"{agent_id}: (u) ERROR: Synthesis failed for '{task_name}'.")

                asyncio.create_task(execute_sovereign_task())
            else:
                await manager.broadcast(f"[System] Error: Agent {agent_id} not found in physical matrix.")


@app.post("/api/v1/agent/update")
async def update_agent(update: Dict):
    if "type" not in update:
        update["type"] = "AGENT_UPDATE"

    # HYPER-EXPANSION: Hydrate update with full agent state if missing
    if update["type"] == "AGENT_UPDATE" and "agent_id" in update:
        from backend.core.config import METROPOLIS_AGENTS
        agent = next((a for a in METROPOLIS_AGENTS if a["id"] == update["agent_id"]), None)
        if agent:
            # Merge existing traits and inventory into the broadcast
            update["traits"] = agent.get("traits", [])
            update["inventory"] = agent.get("inventory", {})
            update["x"] = update.get("x", agent.get("x", 0))
            update["y"] = update.get("y", agent.get("y", 0))

    await manager.broadcast(json.dumps(update))
    return {"status": "success"}

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
