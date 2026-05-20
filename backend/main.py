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
from backend.core.real_machine_bridge import RealMachineBridge

app = FastAPI()

# Initialize Metropolis Core Components
quantum_core = QuantumCore()
sentience_engine = SentienceEngine()
system_integrity = SystemIntegrity()
machine_bridge = RealMachineBridge()

# Global System Logs
SYSTEM_LOGS = []

def add_log(message, level="info"):
    timestamp = time.strftime("%Y-%m-%dT%H:%M:%S.000Z", time.gmtime())
    log_entry = f"[{timestamp}] [SimsMerged-v1.3] [Gemini-CLI-Architect] {message}"
    SYSTEM_LOGS.append(log_entry)
    if len(SYSTEM_LOGS) > 100:
        SYSTEM_LOGS.pop(0)
    print(log_entry)

# Enable CORS for all access
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
    asyncio.create_task(security_invader_loop())
    asyncio.create_task(machine_telemetry_loop())

async def machine_telemetry_loop():
    """
    Syncs the QuantumCore with REAL host machine metrics every 5 seconds.
    """
    while True:
        try:
            stats = machine_bridge.get_actual_metrics()
            if "error" not in stats:
                # Inject real data into simulation
                quantum_core.heat = 30.0 + (stats["real_cpu_load"] * 70.0)
                if stats["real_cpu_load"] > 0.9:
                    quantum_core.stability -= 0.01
                add_log(f"HOST_TELEMETRY: CPU_LOAD {stats['real_cpu_load']*100:.1f}% | MEM {stats['real_mem_pct']*100:.1f}%")
        except:
            pass
        await asyncio.sleep(5)

async def security_invader_loop():
    """
    Randomly spawns security threats (invaders) to test Metropolis defenses.
    """
    while True:
        await asyncio.sleep(random.randint(45, 90))
        threat_types = ["Rogue Kernel", "Buffer Overflow Packet", "SQL Injection Sprite", "Unsigned Firmware Update"]
        threat = random.choice(threat_types)
        add_log(f"SECURITY_ALERT: Detected {threat} attempting to breach Sector {random.randint(1,22)}.", "warn")
        if quantum_core.stability > 0.6:
            add_log(f"DEFENSE_SYNC: Bouncers successfully evicted {threat}.", "info")
        else:
            quantum_core.stability -= 0.05
            add_log(f"CRITICAL_FAILURE: {threat} caused 5% stability drop. Emergency Healing Required.", "error")

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

@app.get("/api/machine-heartbeat")
async def get_heartbeat():
    return machine_bridge.get_actual_metrics()

@app.get("/api/agents")
async def get_agents():
    current_attrs = quantum_core.attributes
    if os.path.exists(POPULATION_FILE):
        with open(POPULATION_FILE, "r") as f:
            agents = json.load(f)
    else:
        agents = [{"name": "Default Sim", "age": 0, "energy": 100, "stability": 1.0, "x": 0, "y": 0}]
    for agent in agents:
        if 'cpu_core' not in agent:
            agent['cpu_core'] = random.randint(0, 15)
        decision = sentience_engine.decide(agent, attributes=current_attrs)
        agent['state'] = decision['emotional_state']
        agent['last_action'] = decision['action']
        agent['confidence'] = decision['confidence']
        agent['model'] = decision['model_info']
        agent['watchdog'] = decision['watchdog_status']
        agent['clipboard'] = decision['clipboard_payload']
        integrity_res = system_integrity.process_stability_net(agent.get('stability', 1.0), attributes=current_attrs)
        agent['stability'] = min(1.0, agent.get('stability', 1.0) + integrity_res['recovery_increment'])
        if integrity_res['should_purge'] and agent.get('role') != 'ADMIN':
            add_log(f"PURGE_COMMAND: Clearing low-stability kernel {agent['name']} due to KV_CACHE pressure.")
    quantum_core.update_core_assignment(agents)
    return agents

@app.get("/api/quantum-tick")
async def quantum_tick(task_id: str = None):
    if task_id:
        db_path = os.path.join(os.path.dirname(__file__), "data", "ai_attributes.json")
        if os.path.exists(db_path):
            with open(db_path, "r", encoding="utf-8") as f:
                db = json.load(f)
                task_data = db.get(task_id)
                if task_data:
                    attr_map = {item['id']: item['val'] for item in task_data}
                    quantum_core.update_attributes(attr_map)
                    add_log(f"Quantum Core Synchronized with {task_id} attributes.")
    metrics = quantum_core.cycle()
    return {"status": "synchronized", "data": metrics}

@app.get("/api/trajectories")
async def get_trajectories():
    return [
        {"from": "CPU", "to": "RAM", "protocol": "BUS", "color": "#00ff00"},
        {"from": "CPU", "to": "GPU", "protocol": "BUS", "color": "#ff00ff"},
        {"from": "CPU", "to": "MODEM", "protocol": "TCP/IP", "color": "#00ffff"},
        {"from": "CPU", "to": "LLM", "protocol": "BUS", "color": "#00ffff"}
    ]

@app.get("/api/logs")
async def get_logs():
    return SYSTEM_LOGS[-20:]

@app.get("/api/research-features")
async def get_research_features():
    db_path = os.path.join(os.path.dirname(__file__), "data", "ai_attributes.json")
    if os.path.exists(db_path):
        with open(db_path, "r", encoding="utf-8") as f:
            return json.load(f)
    return {"error": "AI attributes database not found"}

@app.get("/api/hardware")
async def get_hardware_specs():
    specs_path = os.path.join(os.path.dirname(__file__), "data", "hardware_specs.json")
    if os.path.exists(specs_path):
        with open(specs_path, "r", encoding="utf-8") as f:
            return json.load(f)
    return {"error": "Hardware specifications not found"}

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
