from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import asyncio
import time
import os
import json
import random
from backend.core.quantum_core import QuantumCore
from backend.core.agent_sentience import SentienceEngine
from backend.core.system_integrity import SystemIntegrity

app = FastAPI()

# Initialize Metropolis Core Components
quantum_core = QuantumCore()
sentience_engine = SentienceEngine()
system_integrity = SystemIntegrity()

# Global System Logs
SYSTEM_LOGS = []

def add_log(message):
    timestamp = time.strftime("%Y-%m-%dT%H:%M:%S.000Z", time.gmtime())
    log_entry = f"[{timestamp}] [SimsMerged-v1.3] [Gemini-CLI-Architect] {message}"
    SYSTEM_LOGS.append(log_entry)
    if len(SYSTEM_LOGS) > 100:
        SYSTEM_LOGS.pop(0)
    print(log_entry)

# Enable CORS for file:// access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

POPULATION_FILE = os.path.join(os.path.dirname(__file__), "..", "agents_population.json")

@app.on_event("startup")
async def startup_event():
    add_log("System Startup: Metropolis Authority Online.")
    asyncio.create_task(auto_growth_loop())

async def auto_growth_loop():
    """
    Simulates 'Auto-Growth' by adding a random node to the grid every 60 seconds if stability is > 80%.
    """
    while True:
        await asyncio.sleep(60)
        metrics = quantum_core.cycle()
        stability = metrics.get("stability", 0)
        if stability > 0.8:
            add_log("Auto-Growth Triggered: Stability optimal (> 80%). Adding new node...")
        else:
            add_log(f"Auto-Growth Skipped: Stability too low ({stability*100:.1f}%).")

@app.get("/api/agents")
async def get_agents():
    """
    Returns the current population of agents.
    Now includes research-driven behavioral decisions.
    """
    current_attrs = quantum_core.attributes
    
    if os.path.exists(POPULATION_FILE):
        with open(POPULATION_FILE, "r") as f:
            agents = json.load(f)
    else:
        agents = [{"name": "Default Sim", "age": 0, "energy": 100, "stability": 1.0, "x": 0, "y": 0}]
        
    for agent in agents:
        decision = sentience_engine.decide(agent, attributes=current_attrs)
        agent['state'] = decision['emotional_state']
        agent['last_action'] = decision['action']
        agent['confidence'] = decision['confidence']
        
        # Apply stability recovery if in a Sanctuary (HOSPITAL)
        # We'd check position here in a full sim, for now, we apply global recovery based on Integrity
        integrity_res = system_integrity.process_stability_net(agent.get('stability', 1.0), attributes=current_attrs)
        agent['stability'] = min(1.0, agent.get('stability', 1.0) + integrity_res['recovery_increment'])
        
        if integrity_res['should_purge'] and agent['role'] != 'ADMIN':
            add_log(f"PURGE_COMMAND: Clearing low-stability kernel {agent['name']} due to KV_CACHE pressure.")
            # In a full simulation, we'd remove the agent here.
        
    return agents

@app.get("/api/quantum-tick")
async def quantum_tick(task_id: str = None):
    """
    Exposes the system tick cycle and current stability metrics.
    If task_id is provided, it updates core attributes from the research DB.
    """
    if task_id:
        db_path = os.path.join(os.path.dirname(__file__), "data", "ai_attributes.json")
        if os.path.exists(db_path):
            with open(db_path, "r", encoding="utf-8") as f:
                db = json.load(f)
                task_data = db.get(task_id)
                if task_data:
                    # Convert list of dicts to flat KV pair
                    attr_map = {item['id']: item['val'] for item in task_data}
                    quantum_core.update_attributes(attr_map)
                    add_log(f"Quantum Core Synchronized with {task_id} attributes.")

    metrics = quantum_core.cycle()
    return {
        "status": "synchronized",
        "data": metrics
    }

@app.get("/api/trajectories")
async def get_trajectories():
    """
    Returns a list of active 'Packet Flows' between districts (mocked for now).
    """
    return [
        {"from": "CPU", "to": "RAM", "protocol": "BUS", "color": "#00ff00"},
        {"from": "CPU", "to": "GPU", "protocol": "BUS", "color": "#ff00ff"},
        {"from": "CPU", "to": "MODEM", "protocol": "TCP/IP", "color": "#00ffff"},
        {"from": "CPU", "to": "LLM", "protocol": "BUS", "color": "#00ffff"}
    ]

@app.get("/api/logs")
async def get_logs():
    """
    Returns the last 20 system log messages.
    """
    return SYSTEM_LOGS[-20:]

@app.get("/api/research-features")
async def get_research_features():
    """
    Serves the massive 40,500-parameter AI attributes database mapped to the 2700 tasks.
    """
    db_path = os.path.join(os.path.dirname(__file__), "data", "ai_attributes.json")
    if os.path.exists(db_path):
        with open(db_path, "r", encoding="utf-8") as f:
            return json.load(f)
    return {"error": "AI attributes database not found"}

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)