# TIMESTAMP: 2026-06-08T10:15:00Z
# PROJECT_ID: SimsMerged-v1.4.2
# AGENT_ID: Gemini-CLI-Architect-Fixer

from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import os
import sys
import datetime
import json

# Path resolution
sys.path.append(os.getcwd())
sys.path.append(os.path.join(os.getcwd(), "backend"))
from core.chrono_layer import chronos
from core.orchestrator import AgentCityOrchestrator
# ...

@app.get("/api/chrono-status")
async def get_chrono_status():
    """Returns the current voting epoch, turn, and phase."""
    return chronos.get_chronos_state()

from core.registry_bridge import RegistryBridge
from core.agent_registrar import AgentRegistrar
from core.telemetry_monitor import TelemetryMonitor
from core.road_builder import RoadBuilder
from core.agent_container import AgentContainerManager
from core.zoning_manager import ZoningManager
from core.trust_layer import TrustLayer
from core.sbi_monitor import SBIMonitor
from tools.task_mgr_mini import get_process_summary, kill_process

app = FastAPI(title="SimAgentCity API")

# Add CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- CHAT ENGINE (POLLING BASED) ---
CHAT_LOG_PATH = os.path.join(os.getcwd(), "chat_logs.json")

@app.post("/chat")
async def post_chat(req: dict):
    entry = {
        "timestamp": datetime.datetime.now().strftime("%H:%M:%S"),
        "agent": req.get("agent", "User"),
        "message": req.get("message", "")
    }
    logs = []
    if os.path.exists(CHAT_LOG_PATH):
        try:
            with open(CHAT_LOG_PATH, "r") as f:
                logs = json.load(f)
        except: logs = []
    logs.append(entry)
    with open(CHAT_LOG_PATH, "w") as f:
        json.dump(logs[-50:], f, indent=2)
    return {"status": "SUCCESS"}

@app.get("/chat")
async def get_chat():
    # Auto-heartbeat
    heartbeat = {
        "timestamp": datetime.datetime.now().strftime("%H:%M:%S"),
        "agent": "SYSTEM",
        "message": "CONNECTION_ALIVE"
    }
    if not os.path.exists(CHAT_LOG_PATH):
        return {"logs": [heartbeat]}
    with open(CHAT_LOG_PATH, "r") as f:
        try: logs = json.load(f)
        except: logs = []
    return {"logs": logs[-50:] + [heartbeat]}

# --- ENDPOINTS ---
@app.get("/api/machine-heartbeat")
async def get_heartbeat():
    return {"status": "ONLINE", "timestamp": datetime.datetime.now().isoformat()}

@app.get("/api/metropolis-state")
async def get_metropolis_state():
    return {"state": "GENESIS_PHASE", "active_agents": 8}

@app.post("/api/metropolis-state")
async def post_metropolis_state():
    return {"status": "ACKNOWLEDGED"}

@app.get("/api/network-status")
async def get_network_status(): return {"status": "ONLINE"}

@app.get("/api/physical-status")
async def get_physical_status(): return {"status": "ONLINE"}

@app.get("/api/hardware")
async def get_hardware(): return {"status": "ONLINE"}

@app.get("/api/evolution-project")
async def get_evolution(): return {"status": "ACTIVE"}

@app.get("/api/machine-hardware-telemetry")
async def get_hardware_telemetry():
    return telemetry.get_hardware_bus()

@app.post("/api/bank/mint")
async def mint_currency(req: dict):
    amount = req.get("amount", 0)
    orchestrator.ledger.mint("System", "SPRITE", amount)
    return {"status": "SUCCESS", "new_balance": orchestrator.ledger.get_balance("System", "SPRITE")}

@app.get("/api/ledger-status")
async def get_ledger_status():
    return {"balance": orchestrator.ledger.get_balance("System", "SPRITE"), "mint_rate": 0.05}

# Initialize Orchestrator on a default workspace
WORKSPACE = os.path.join(os.getcwd(), "city_workspace")
orchestrator = AgentCityOrchestrator(WORKSPACE)
registry = RegistryBridge()
registrar = AgentRegistrar(os.path.join(os.getcwd(), "agents_population.json"))
telemetry = TelemetryMonitor()
roads = RoadBuilder(WORKSPACE)
containers = AgentContainerManager(WORKSPACE)
zoning = ZoningManager(os.path.join(os.getcwd(), "city_zoning.json"))
trust = TrustLayer(os.path.join(os.getcwd(), "trust_graph.json"))
sbi = SBIMonitor(os.path.join(os.getcwd(), "behavior_history.json"))

# Mount Frontend
app.mount("/static", StaticFiles(directory="frontend"), name="static")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
