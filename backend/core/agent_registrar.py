import json
import os

POPULATION_FILE = "../agents_population.json"

def update_agents():
    population = []
    if os.path.exists(POPULATION_FILE):
        try:
            with open(POPULATION_FILE, "r") as f:
                population = json.load(f)
        except Exception:
            pass

    # Evolve agents
    for agent in population:
        agent['age'] = agent.get('age', 0) + 1
        agent['energy'] = max(0, agent.get('energy', 100) - 1)

    with open(POPULATION_FILE, "w") as f:
        json.dump(population, f, indent=4)