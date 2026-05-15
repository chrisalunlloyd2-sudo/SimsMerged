from fastapi import APIRouter
import json
import os

router = APIRouter()
POPULATION_FILE = "../agents_population.json"

@router.get("/agents")
def get_agents():
    if os.path.exists(POPULATION_FILE):
        with open(POPULATION_FILE, "r") as f:
            return json.load(f)
    return []