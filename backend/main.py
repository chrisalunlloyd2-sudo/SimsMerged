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

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)