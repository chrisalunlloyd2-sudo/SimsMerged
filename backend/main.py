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
from backend.core.economy import CyberEconomy
from backend.core.progression import ProgressionEngine

app = FastAPI()

# Initialize Metropolis Core Components
quantum_core = QuantumCore()
sentience_engine = SentienceEngine()
system_integrity = SystemIntegrity()
machine_bridge = RealMachineBridge()
cyber_economy = CyberEconomy()
progression_engine = ProgressionEngine()

# Global System Logs
SYSTEM_LOGS = []

def add_log(message, level="info"):
    timestamp = time.strftime("%Y-%m-%dT%H:%M:%S.000Z", time.gmtime())
    # MANDATORY ATOMIC SIGNATURE: [TIMESTAMP] [PROJECT_ID] [AGENT_ID]
    signature = f"[{timestamp}] [SimsMerged-v1.3] [Gemini-CLI-Architect]"
    log_entry = f"{signature} {message}"
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
        threat_types = ["Rogue Kernel", "Buffer Overflow Packet", "SQL Injection Sprite", "Row Hammer Attack"]
        threat = random.choice(threat_types)

        if threat == "Row Hammer Attack":
            status = quantum_core.trigger_hammer_event()
            add_log(f"SECURITY_ALERT: {threat} detected on Memory Matrix. Status: {status}.", "warn")
            if status == "MITIGATED":
                add_log("DEFENSE_SYNC: Target Row Refresh (TRR) successfully mitigated bit-flip.", "info")
        else:
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

import math
import hashlib

# DePIN Ledger State
LEDGER_FILE = os.path.join(os.path.dirname(__file__), "data", "blockchain_ledger.json")

def generate_block_hash(agent_name, action, prev_hash):
    """
    Generates a real SHA256 hash for the DePIN ledger.
    """
    data = f"{agent_name}{action}{prev_hash}{time.time()}".encode()
    return hashlib.sha256(data).hexdigest()

def record_transaction(agent_name, action):
    """
    Records a cryptographically verified transaction to the DePIN ledger.
    """
    try:
        ledger = []
        if os.path.exists(LEDGER_FILE):
            with open(LEDGER_FILE, "r") as f:
                ledger = json.load(f)
        
        prev_hash = ledger[-1]["hash"] if ledger else "0" * 64
        new_hash = generate_block_hash(agent_name, action, prev_hash)
        
        entry = {
            "index": len(ledger),
            "timestamp": time.time(),
            "agent": agent_name,
            "action": action,
            "prev_hash": prev_hash,
            "hash": new_hash
        }
        ledger.append(entry)
        
        # Maintain only last 1000 blocks for performance
        if len(ledger) > 1000: ledger.pop(0)
        
        with open(LEDGER_FILE, "w") as f:
            json.dump(ledger, f, indent=2)
            
        return new_hash
    except:
        return "HASH_ERROR"

# Scripts Persistence
SCRIPTS_FILE = os.path.join(os.path.dirname(__file__), "data", "automation_scripts.json")

def save_script(agent_name, steps):
    """
    Saves a recorded path as an automation script.
    """
    try:
        scripts = {}
        if os.path.exists(SCRIPTS_FILE):
            with open(SCRIPTS_FILE, "r") as f:
                scripts = json.load(f)
        
        script_id = f"SCRIPT_{agent_name.upper()}_{len(scripts)}"
        scripts[script_id] = {
            "name": f"Routine_{agent_name}",
            "steps": steps,
            "author": agent_name,
            "verified": True
        }
        
        with open(SCRIPTS_FILE, "w") as f:
            json.dump(scripts, f, indent=2)
        return script_id
    except:
        return None

@app.get("/api/agents")
async def get_agents():
    """
    Returns the current population of agents.
    Now supports Real-time Script Recording and Playback (Step 40).
    """
    current_attrs = quantum_core.attributes
    host_stats = machine_bridge.get_actual_metrics()
    
    if "error" in host_stats:
        return [{"name": "HOST_SYNC_ERROR", "stability": 0.1, "x": 0, "y": 0, "role": "KERNEL"}]
        
    agents = []
    procs = host_stats.get("processes", [])
    if isinstance(procs, dict): procs = [procs] 
    
    for i, proc in enumerate(procs):
        angle = (i / len(procs)) * math.pi * 2
        radius = 12
        px = int(math.cos(angle) * radius)
        py = int(math.sin(angle) * radius)
        
        cpu_usage = proc.get("CPU", 0)
        stability = max(0.1, 1.0 - (cpu_usage / 2000.0))
        
        # Assign Vocational Roles
        role = "PROCESS_KERNEL"
        if i % 5 == 0: role = "DOCTOR"
        elif i % 5 == 1: role = "TEACHER"
        
        agent = {
            "id": str(proc.get("Id")),
            "name": proc.get("Name"),
            "age": 0,
            "energy": 100,
            "stability": float(stability),
            "x": px,
            "y": py,
            "role": role,
            "working_set_kb": proc.get("WorkingSet", 0) / 1024
        }
        
        # Sandbox Stability Processing
        raw_stability = agent.get('stability', 1.0)
        isolated_stability = quantum_core.process_agent_stability(agent.get('name'), raw_stability)
        
        decision = sentience_engine.decide(agent, attributes=current_attrs)
        agent['state'] = decision['emotional_state']
        agent['last_action'] = decision['action']
        agent['confidence'] = decision['confidence']
        agent['model'] = decision['model_info']
        agent['watchdog'] = decision['watchdog_status']

        # AWARD XP & LEVEL UP
        xp_gain = 5
        if agent['last_action'] == 'heal' or agent['last_action'] == 'heal_hospital': xp_gain = 25
        elif agent['last_action'] == 'teach': xp_gain = 30
        elif agent['last_action'] == 'negotiate_casino': xp_gain = 50
        
        leveled_city = progression_engine.add_agent_xp(agent['name'], xp_gain)
        if leveled_city:
            add_log(f"CITY_ASCENSION: Metropolis reached Level {progression_engine.global_level}! Next unlock in progress.")
            
        p_data = progression_engine.agent_levels.get(agent['name'])
        agent['level'] = p_data['level']
        agent['title'] = p_data['title']
        
        # SCRIPT EVOLUTION (Step 40)
        if decision.get('recording'):
            agent['status_msg'] = "RECORDING_PATH"
            # If recording reaches 10 steps, persist and "Graduate" to Scripted Mode
            steps = sentience_engine.active_recordings.get(agent['id'], [])
            if len(steps) >= 10:
                script_id = save_script(agent['name'], steps)
                if script_id:
                    add_log(f"GENESIS_EVOLUTION: {agent['name']} graduated to scripted automation: {script_id}", "info")
                    agent['script_id'] = script_id
        
        if decision['action'] == 'PLAYBACK':
            agent['status_msg'] = f"EXECUTING_{decision['script_id']}"

        # VOCATIONAL LOGIC
        if agent['last_action'] == 'heal':
            add_log(f"SOCIAL_SYNC: {agent['name']} (DOCTOR) restoring stability in Sector 0.")
            quantum_core.stability = min(1.0, quantum_core.stability + 0.01)
        elif agent['last_action'] == 'teach':
            add_log(f"SOCIAL_SYNC: {agent['name']} (TEACHER) aligning agent weights.")
            agent['confidence'] = min(1.0, agent['confidence'] + 0.1)
        elif agent['last_action'] == 'heal_hospital':
            add_log(f"MED-BAY: {agent['name']} admitted to HOSPITAL for critical recovery.")
            isolated_stability = min(1.0, isolated_stability + 0.2)
        elif agent['last_action'] == 'negotiate_casino':
            add_log(f"CASINO: {agent['name']} is negotiating assets at the Hotel Casino.")
        
        # Real DePIN Hashing
        agent['last_hash'] = record_transaction(agent['name'], agent['last_action'])
        
        # Speculative Execution Failure
        if quantum_core.speculative_execution_active and agent['last_action'] == 'process':
            if random.random() > quantum_core.branch_accuracy:
                add_log(f"SPECULATIVE_MISS: Branch failure on process {agent['name']}.", "error")
                isolated_stability *= 0.8
        
        # Stability recovery logic
        integrity_res = system_integrity.process_stability_net(isolated_stability, attributes=current_attrs)
        agent['stability'] = min(1.0, isolated_stability + integrity_res['recovery_increment'])
        
        agents.append(agent)
            
    quantum_core.update_core_assignment(agents)
    # Update RAM Pressure state
    quantum_core.memory_pressure_active = quantum_core.ram_load > 0.7
    
    return agents

@app.post("/api/flush-memory")
async def flush_memory():
    """
    Simulates a memory write-back to the Storage Hive, clearing dirty bits.
    """
    count = quantum_core.flush_dirty_pages()
    add_log(f"MEMORY_FLUSH: Synchronized {count} dirty pages to Storage Hive.")
    return {"status": "flushed", "pages": count}

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
    economy_data = cyber_economy.process_tick()
    progression_data = progression_engine.get_state()
    
    # Apply Progression Buffs to live metrics
    metrics['stability'] = min(1.0, metrics['stability'] * progression_data['buffs']['stability_recovery'])
    
    metrics['economy'] = economy_data
    metrics['progression'] = progression_data
    # Include dirty pages in metrics
    metrics['dirty_pages'] = [list(p) for p in quantum_core.dirty_pages]
    metrics['weather'] = system_integrity.current_weather
    return {"status": "synchronized", "data": metrics}

@app.get("/api/trajectories")
async def get_trajectories():
    """
    Generates automated dynamic vehicle traffic and data pathfinding.
    """
    trajectories = []
    
    # Static data flows
    trajectories.extend([
        {"from": "CPU", "to": "RAM", "protocol": "BUS", "color": "#00ff00"},
        {"from": "CPU", "to": "GPU", "protocol": "BUS", "color": "#ff00ff"},
        {"from": "CPU", "to": "MODEM", "protocol": "TCP/IP", "color": "#00ffff"},
        {"from": "CPU", "to": "LLM", "protocol": "BUS", "color": "#00ffff"}
    ])
    
    # Dynamic automated vehicle traffic
    num_vehicles = random.randint(3, 8)
    vehicle_types = [
        {"protocol": "CAR", "color": "#ffaa00", "speed": 0.01},
        {"protocol": "BUS", "color": "#4facfe", "speed": 0.005},
        {"protocol": "TRUCK", "color": "#ffffff", "speed": 0.003}
    ]
    
    nodes = ["HOUSE", "BANK", "HOSPITAL", "PLANT", "SCHOOL"]
    
    for _ in range(num_vehicles):
        v = random.choice(vehicle_types)
        f = random.choice(nodes)
        t = random.choice([n for n in nodes if n != f])
        
        # Add a dynamic path entry that the frontend engine can parse
        trajectories.append({
            "from": f,
            "to": t,
            "protocol": v["protocol"],
            "color": v["color"],
            "speed": v["speed"]
        })
        
    return trajectories

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
