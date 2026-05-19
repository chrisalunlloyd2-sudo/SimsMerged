from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import asyncio
import time
import os
import json
from backend.core.quantum_core import QuantumCore
from backend.core.agent_sentience import SentienceEngine

app = FastAPI()

# Initialize Metropolis Core Components
quantum_core = QuantumCore()
sentience_engine = SentienceEngine()

# Enable CORS for file:// access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

POPULATION_FILE = os.path.join(os.path.dirname(__file__), "..", "agents_population.json")

@app.get("/api/agents")
async def get_agents():
    if os.path.exists(POPULATION_FILE):
        with open(POPULATION_FILE, "r") as f:
            return json.load(f)
    return [{"name": "Default Sim", "age": 0, "energy": 100}]

@app.get("/api/quantum-tick")
async def quantum_tick():
    """
    Exposes the system tick cycle and current stability metrics.
    """
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

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)