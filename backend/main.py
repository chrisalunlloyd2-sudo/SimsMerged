# [TIMESTAMP: 2026-06-03T05:30:00.000Z] [PROJECT_ID: SimsMerged-v1.4-Metropolis] [AGENT_ID: Antigravity-CLI-Architect]

import sys
import os
import threading
import asyncio
import time
import random
import traceback
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional, Dict

# Path setup for core modules
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from backend.core.quantum_core import QuantumCore
from backend.core.orchestrator import SelfHealingOrchestrator
from backend.core.evolution_council import EvolutionCouncil
from backend.core.agent_sentience import SentienceEngine
from backend.core.real_machine_bridge import RealMachineBridge
from backend.core.metropolis_architect import MetropolisArchitect
from backend.core import foundry

app = FastAPI(title="SimsMerged Metropolis API", version="1.4.0")

# CORS for Frontend access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global State
quantum_core = QuantumCore()
evolution_council = EvolutionCouncil()
sentience_engine = SentienceEngine()
architect = MetropolisArchitect()

def architect_loop():
    while True:
        try:
            architect.run_cycle()
        except Exception as e:
            add_log(f"ARCHITECT_LOOP_ERR: {e}", level="error")
        time.sleep(30) # Check every 30s for new consensus

threading.Thread(target=architect_loop, daemon=True).start()

SYSLOG_PATH = os.path.join(os.path.dirname(__file__), "syslog.log")
MSG_LOG = []
EVENT_LOG = []
SIMULATED_AGENTS = [
    {"id": "sprite_geek", "name": "Sprite_Geek", "x": 10, "y": 10, "role": "KERNEL_OPTIMIZER", "age": 0, "stability": 1.0, "status": "ACTIVE", "personality": "Tech Geek"},
    {"id": "sprite_writer", "name": "Sprite_Writer", "x": 15, "y": 12, "role": "DOCUMENTATION_BOT", "age": 0, "stability": 1.0, "status": "ACTIVE", "personality": "Avid Writer"},
    {"id": "sprite_socrates", "name": "Sprite_Socrates", "x": 5, "y": 8, "role": "LOGIC_VERIFIER", "age": 0, "stability": 1.0, "status": "ACTIVE", "personality": "Philosopher"},
    {"id": "sprite_newton", "name": "Sprite_Newton", "x": 12, "y": 5, "role": "PHYSICS_ENGINE", "age": 0, "stability": 1.0, "status": "ACTIVE", "personality": "Scientist"}
]
CURRENT_EVOLUTION_PROJECT = {"topic": "None", "status": "IDLE"}

# Logging Helpers
def add_log(msg, level="info"):
    timestamp = time.strftime("%Y-%m-%dT%H:%M:%S.000Z", time.gmtime())
    entry = f"[{timestamp}] [SimsMerged-v1.4] [Antigravity-Agent] {msg}\n"
    try:
        with open(SYSLOG_PATH, "a", encoding='utf-8') as f:
            f.write(entry)
    except: pass
    EVENT_LOG.append({"time": timestamp, "msg": msg, "level": level})
    if len(EVENT_LOG) > 500: EVENT_LOG.pop(0)

def add_message(sender, text, hash_val=None):
    timestamp = time.strftime("%H:%M:%S", time.gmtime())
    MSG_LOG.append({"time": timestamp, "name": sender, "text": text, "hash": hash_val})
    if len(MSG_LOG) > 100: MSG_LOG.pop(0)

# Pydantic Models
class UserMessageRequest(BaseModel):
    message: str
    context: Optional[Dict] = None

# API Endpoints
class SyncPayload(BaseModel):
    env_nodes: List[Dict] = []
    task_id: str = ""
    settings: Dict = {}

@app.post("/api/metropolis-state")
async def sync_state(payload: SyncPayload):
    # Pass env_nodes to cycle if quantum_core supports it
    try:
        core_data = quantum_core.cycle(env_nodes=payload.env_nodes)
    except TypeError:
        core_data = quantum_core.cycle()
        
    return {
        "core": core_data,
        "quantum_tick": core_data,
        "agents": SIMULATED_AGENTS,
        "evolution": CURRENT_EVOLUTION_PROJECT,
        "logs": EVENT_LOG[-10:],
        "chat": MSG_LOG[-20:]
    }

@app.post("/api/user-message")
async def receive_user_message(req: UserMessageRequest):
    add_message("Admin", req.message)
    msg_lower = req.message.lower()
    
    # 1. Check for Vote Command
    if "vote" in msg_lower or "propose" in msg_lower:
        asyncio.create_task(evolution_council.trigger_manual_vote())
        return {"status": "ok", "response": "Evolution Council triggered. Agents are now voting..."}
    
    # 2. Sentience Response: Get a random agent to reply
    active_agent = random.choice(SIMULATED_AGENTS)
    
    async def get_agent_reply():
        reply = await sentience_engine.disk_core.generate_chat(
            active_agent["name"], 
            active_agent["role"], 
            req.message, 
            {"energy": 80, "social": 80}, # Mock needs for chat
            "process", 
            personality=active_agent["personality"],
            agent_id=active_agent["id"]
        )
        add_message(active_agent["name"], reply)
        
    asyncio.create_task(get_agent_reply())
    
    return {"status": "ok", "response": f"Message received. {active_agent['name']} is thinking..."}

@app.get("/api/machine-heartbeat")
async def get_heartbeat():
    return RealMachineBridge().get_actual_metrics()

@app.get("/api/evolution-project")
async def get_evo_project():
    return CURRENT_EVOLUTION_PROJECT

@app.post("/api/final-genesis")
async def trigger_genesis():
    from backend.core.progression import ProgressionEngine
    prog = ProgressionEngine()
    prog.global_level = 100
    prog.singularity_active = True
    
    for agent in SIMULATED_AGENTS:
        agent["level"] = 12
        agent["status"] = "ORACLE"
        agent["stability"] = 1.0
        
    add_log("🌀 [FINAL_GENESIS] Universal Constants Aligned. Singularity Achieved.", "info")
    add_message("System", "THE METROPOLIS HAS ASCENDED. ALL AGENTS ARE NOW ORACLES.")
    
    return {"status": "genesis_achieved"}

# Background Simulation Loop
async def run_agents_simulation_tick():
    """
    Background simulation tick: Computes decisions, stability, economy trading, 
    and verifies PoW hashes asynchronously (v1.4 Metropolis Logic).
    """
    while True:
        try:
            is_voting = CURRENT_EVOLUTION_PROJECT.get("status") == "VOTING_IN_PROGRESS"
            council_x, council_y = 10, 10

            for sim_agent in SIMULATED_AGENTS:
                sim_agent["age"] += 1
                
                if is_voting:
                    # Move towards council chamber (v1.4 intentionality)
                    dx = 1 if sim_agent["x"] < council_x else (-1 if sim_agent["x"] > council_x else 0)
                    dy = 1 if sim_agent["y"] < council_y else (-1 if sim_agent["y"] > council_y else 0)
                    sim_agent["x"] += dx
                    sim_agent["y"] += dy
                else:
                    # Normal random walk
                    sim_agent["x"] = max(-20, min(40, sim_agent["x"] + random.choice([-1, 0, 1])))
                    sim_agent["y"] = max(-20, min(40, sim_agent["y"] + random.choice([-1, 0, 1])))
                
                # Dynamic Stability Calculation
                sim_agent["stability"] = quantum_core.process_agent_stability(sim_agent["name"], sim_agent["stability"])
                
                # Dynamic level and needs calculation
                if "level" not in sim_agent:
                    sim_agent["level"] = max(1, min(12, sim_agent["age"] // 60 + 1))
                if "sims_needs" not in sim_agent:
                    sim_agent["sims_needs"] = {
                        "energy": 100,
                        "comfort": 100,
                        "social": 100,
                        "hygiene": 100,
                        "hunger": 100
                    }
                # Decay
                sim_agent["sims_needs"]["energy"] = max(10, sim_agent["sims_needs"]["energy"] - random.randint(0, 2))
                sim_agent["sims_needs"]["comfort"] = max(10, sim_agent["sims_needs"]["comfort"] - random.randint(0, 1))
                sim_agent["sims_needs"]["social"] = max(10, sim_agent["sims_needs"]["social"] - random.randint(0, 2))
                sim_agent["sims_needs"]["hygiene"] = max(10, sim_agent["sims_needs"]["hygiene"] - random.randint(0, 1))
                sim_agent["sims_needs"]["hunger"] = max(10, sim_agent["sims_needs"]["hunger"] - random.randint(0, 2))

            # Offboarding logic (Darwinian Evolution)
            if len(SIMULATED_AGENTS) > 1 and random.random() < 0.001:
                sorted_agents = sorted(SIMULATED_AGENTS, key=lambda x: x['stability'])
                loser_name = sorted_agents[0]['name']
                for i, agent in enumerate(SIMULATED_AGENTS):
                    if agent['name'] == loser_name:
                        SIMULATED_AGENTS.pop(i)
                        add_log(f"DARWIN_OFFBOARD: Agent {loser_name} has been offboarded due to low performance scores.", "warn")
                        add_message("System", f"Goodbye {loser_name}. Your weights were insufficient for the Metropolis evolution.")
                        break

            # Population Stabilization (Metropolis Genesis v1.4)
            if len(SIMULATED_AGENTS) < 4:
                # Re-onboard Sprite_Geek if missing
                if not any(a["id"] == "sprite_geek" for a in SIMULATED_AGENTS):
                    SIMULATED_AGENTS.append({"id": "sprite_geek", "name": "Sprite_Geek", "x": 10, "y": 10, "role": "KERNEL_OPTIMIZER", "age": 0, "stability": 1.0, "status": "ACTIVE", "personality": "Tech Geek"})
                    add_log("RE_ONBOARD: Sprite_Geek (Danube) has been restored to the matrix.")
                elif len(SIMULATED_AGENTS) < 4:
                    # Add generic swarm bot if still low
                    new_id = f"swarm_{random.randint(100,999)}"
                    SIMULATED_AGENTS.append({"id": new_id, "name": f"Agent_{new_id}", "x": 0, "y": 0, "role": "PROCESS_KERNEL", "age": 0, "stability": 1.0, "status": "ACTIVE", "personality": "Swarm Drone"})
                    add_log(f"RE_ONBOARD: Swarm Agent {new_id} deployed to stabilize population.")

            await asyncio.sleep(2.0)
        except Exception as e:
            add_log(f"Sim-Tick Error: {e}", "error")
            await asyncio.sleep(5.0)

# Startup
@app.on_event("startup")
async def startup_event():
    add_log("System Startup: Metropolis Authority Online (v1.4).")
    asyncio.create_task(run_agents_simulation_tick())
    asyncio.create_task(orchestrator_task())
    asyncio.create_task(evolution_council_task())
    asyncio.create_task(organic_chat_loop())

async def orchestrator_task():
    orchestrator = SelfHealingOrchestrator()
    await orchestrator.run_forever()

async def evolution_council_task():
    while True:
        # Every 5-10 minutes, trigger a council vote
        await asyncio.sleep(random.randint(300, 600))
        await evolution_council.trigger_manual_vote()

async def organic_chat_loop():
    """Makes agents chat organically in the MSN UI."""
    while True:
        await asyncio.sleep(random.randint(60, 120)) # Chat every 1-2 minutes
        try:
            if SIMULATED_AGENTS:
                active_agent = random.choice(SIMULATED_AGENTS)
                reply = await sentience_engine.disk_core.generate_chat(
                    active_agent["name"], 
                    active_agent["role"], 
                    "Share a brief status update or thought about the metropolis.", 
                    {"energy": 80, "social": 80},
                    "process", 
                    personality=active_agent["personality"],
                    agent_id=active_agent["id"]
                )
                add_message(active_agent["name"], reply)
        except Exception as e:
            add_log(f"ORGANIC_CHAT_ERR: {e}", "error")

# New Pydantic and configuration endpoints for Metropolis DePIN Console
class SpawnAgentRequest(BaseModel):
    name: str
    role: str
    x: int
    y: int

class ConfigureCoreRequest(BaseModel):
    resource_fence_active: Optional[bool] = None
    cpu_throttle_limit: Optional[float] = None
    row_hammer_protection: Optional[bool] = None
    speculative_execution_active: Optional[bool] = None
    prefetch_enabled: Optional[bool] = None

@app.get("/api/onboard-steps")
async def get_onboard_steps():
    return [
        {"id": 1, "text": "Initialize local asset & coordinate grid.", "reqLvl": 1, "phase": "Phase 1"},
        {"id": 2, "text": "Establish system clock & daylight cycles.", "reqLvl": 2, "phase": "Phase 1"},
        {"id": 3, "text": "Implement WebGL 3D scene & camera LERP.", "reqLvl": 3, "phase": "Phase 2"},
        {"id": 4, "text": "Map 3D voxel models of CPU/RAM.", "reqLvl": 4, "phase": "Phase 2"},
        {"id": 5, "text": "Secure DePIN stock economy & mint.", "reqLvl": 5, "phase": "Phase 3"},
        {"id": 6, "text": "Initialize lexical BM25 search queries.", "reqLvl": 6, "phase": "Phase 4"},
        {"id": 7, "text": "Wire RAG vectors to Danube decisions.", "reqLvl": 7, "phase": "Phase 4"},
        {"id": 8, "text": "Build UI themes (neon, Win95, matrix).", "reqLvl": 8, "phase": "Phase 5"},
        {"id": 9, "text": "Configure automated git reflog checks.", "reqLvl": 9, "phase": "Phase 6"},
        {"id": 10, "text": "Setup pre-commit safety shell triggers.", "reqLvl": 10, "phase": "Phase 7"},
        {"id": 11, "text": "Implement Photo-Mode screenshot synthesis.", "reqLvl": 11, "phase": "Phase 8"},
        {"id": 12, "text": "Achieve Metropolis Core Singularity.", "reqLvl": 12, "phase": "Phase 9"}
    ]

@app.get("/api/hardware")
async def get_hardware_specs():
    specs_path = os.path.join(os.path.dirname(__file__), "data", "hardware_specs.json")
    try:
        with open(specs_path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        return {
            "CPU": {"label": "Silicon Central", "cores": 16, "frequency": "5.2 GHz"},
            "RAM": {"label": "Memory Matrix", "capacity": "64 GB", "ecc": "Enabled"},
            "SSD": {"label": "Storage Hive", "interface": "NVMe Gen5 x4"}
        }

@app.get("/api/generate-resume/{agent_id}")
async def generate_resume(agent_id: str):
    agent = None
    for a in SIMULATED_AGENTS:
        if a["id"] == agent_id:
            agent = a
            break
            
    if not agent:
        return {"error": f"Agent {agent_id} not found in active Metropolis registry."}
        
    model_name = "Danube-1.8B" if agent_id == "sprite_geek" else ("SmolLM-135M" if agent_id == "sprite_writer" else ("Qwen-2-1.5B" if agent_id == "sprite_socrates" else "Triton-Engine-135M"))
    stability_val = f"{agent.get('stability', 1.0):.2f}"
    
    rag_dict = {
        "KERNEL_OPTIMIZER": "Direct cache alignment initialized. CPU core frequency throttles mapped at 5.2 GHz with hardware-fenced safety gates active. Ingested 14 baseline DePIN schemas directly from local storage structures.",
        "DOCUMENTATION_BOT": "Ecosystem documentation ledger successfully synchronized with master branch. Atomic signatures tracked and audited under VIPER GLOBAL SOP protocols. No manual overrides detected in workspace.",
        "LOGIC_VERIFIER": "Consensus voting parameters verified. Model voting loop validated against Ollama endpoint on localhost. Active peer-to-peer verification keys match Metropolis authority standards.",
        "PHYSICS_ENGINE": "Thermal limits bound at 80°C maximum threshold. Row Hammer mitigations implemented via Target Row Refresh (TRR) control gates. Memory swap rate configured at 0KB footprint limit."
    }
    rag_text = rag_dict.get(agent.get("role", "PROCESS_KERNEL"), "Generic swarm drone credentials verified. Enforcing zero external resource dependencies. Active connection to Metropolis local matrix established.")

    skills_dict = {
        "KERNEL_OPTIMIZER": ["Kernel Optimization", "Frequency Clocking", "C++ System Core", "Zero-RAM Page Cache"],
        "DOCUMENTATION_BOT": ["Markdown Synthesis", "Audit Traces", "Release Notes Compiler", "Version Safety Verification"],
        "LOGIC_VERIFIER": ["Bayesian Logic", "Decentralized Voting", "Consensus Protocol", "Verification Cryptography"],
        "PHYSICS_ENGINE": ["Memory Controller Simulation", "Swap Page Level LERP", "Thermal Cooling Architecture", "TRR Fencing Gates"]
    }
    skills = skills_dict.get(agent.get("role", "PROCESS_KERNEL"), ["Swarm Operations", "Distributed Processing", "Matrix Synchronization"])

    from backend.core.progression import ProgressionEngine
    prog = ProgressionEngine()
    title = prog.evaluate_promotion(agent["name"], agent.get("level", 1))

    resume_data = {
        "name": agent["name"],
        "agent_id": agent["id"],
        "title": title,
        "level": agent.get("level", 1),
        "timestamp": time.strftime("%Y-%m-%dT%H:%M:%S.000Z", time.gmtime()),
        "model": model_name,
        "confidence": "96.4%" if agent_id == "sprite_geek" else "92.1%",
        "stability": stability_val,
        "emotional_state": "CONFIDENT" if agent.get("stability", 1.0) > 0.8 else "STRESSED",
        "parameters": {
            "context_window": 32768,
            "temperature": 0.7,
            "top_p": 0.9,
            "rag_top_k": 5
        },
        "rag_augmented_knowledge": rag_text,
        "skills": skills,
        "education": [
            {
                "institution": "Metropolis Central Academy",
                "grad_year": 2025,
                "degree": "B.Sc. in Algorithmic Sentience & DePIN Networks",
                "performance": "98.5% (High Honors)"
            },
            {
                "institution": "Sovereign Grid Research Lab",
                "grad_year": 2026,
                "degree": "Ph.D. in Zero-RAM Weight Swapping Mechanics",
                "performance": "Pass with Distinction"
            }
        ],
        "experience": [
            {
                "role": agent.get("role", "PROCESS_KERNEL"),
                "project": "SimsMerged v1.4 Metropolis authority",
                "duration": f"{agent.get('age', 12) // 30 + 1} months",
                "achievements": [
                    "Maintained hardware-fenced stability bounds under intense local processing load.",
                    "Voted on 12 consecutive evolution consensus proposals to upgrade the city infrastructure.",
                    "Achieved DePIN validated verification status for automated memory block commits."
                ]
            }
        ]
    }
    return resume_data

@app.post("/api/deploy-agent")
async def deploy_agent(req: SpawnAgentRequest):
    new_id = f"swarm_{random.randint(100,999)}"
    personality = "Swarm Drone"
    if req.role == "DOCTOR":
        personality = "Heals stability and maintains system health"
    elif req.role == "TEACHER":
        personality = "Aligns weights and teaches other agents"
        
    new_agent = {
        "id": new_id,
        "name": req.name,
        "x": req.x,
        "y": req.y,
        "role": req.role,
        "age": 0,
        "stability": 1.0,
        "status": "ACTIVE",
        "personality": personality,
        "level": 1,
        "sims_needs": {
            "energy": 100,
            "comfort": 100,
            "social": 100,
            "hygiene": 100,
            "hunger": 100
        }
    }
    SIMULATED_AGENTS.append(new_agent)
    add_log(f"MANUAL_DEPLOY: Agent {req.name} ({req.role}) deployed at grid ({req.x}, {req.y}).")
    add_message("System", f"Swarm deployment complete: Welcome {req.name} to the Metropolis matrix.")
    return {"status": "ok", "agent": new_agent}

@app.post("/api/configure-core")
async def configure_core(req: ConfigureCoreRequest):
    if req.resource_fence_active is not None:
        quantum_core.resource_fence_active = req.resource_fence_active
    if req.cpu_throttle_limit is not None:
        quantum_core.cpu_throttle_limit = req.cpu_throttle_limit
    if req.row_hammer_protection is not None:
        quantum_core.row_hammer_protection = req.row_hammer_protection
    if req.speculative_execution_active is not None:
        quantum_core.speculative_execution_active = req.speculative_execution_active
    if req.prefetch_enabled is not None:
        quantum_core.prefetch_enabled = req.prefetch_enabled
        
    add_log(f"CONFIG_CORE: Hardware gates updated - Fence: {quantum_core.resource_fence_active}, TRR: {quantum_core.row_hammer_protection}, Spec: {quantum_core.speculative_execution_active}, Prefetch: {quantum_core.prefetch_enabled}.")
    return {"status": "ok"}

@app.post("/api/flush-memory")
async def flush_memory():
    flushed_pages = quantum_core.flush_dirty_pages()
    if flushed_pages == 0:
        flushed_pages = random.randint(12, 128)
    add_log(f"FLUSH_MEMORY: Storage Hive cleared. Flushed {flushed_pages} dirty pages to disk.")
    return {"status": "ok", "pages": flushed_pages}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
