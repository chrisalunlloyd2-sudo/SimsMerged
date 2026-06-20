# [TIMESTAMP: 2026-06-08T09:15:00.000Z] [PROJECT_ID: SimsMerged-v1.4.2] [AGENT_ID: viper_cli-architectssj4]

import os
import json
import time
import asyncio
import random
from typing import List, Dict, Optional
from .config import SSD_SANDBOX_PATH, add_log, add_message
from .model_orchestrator import model_orchestrator
from .execution_engine import execution_sandbox

FACTORIES_DIR = os.path.join(SSD_SANDBOX_PATH, "neural_factories")
METRICS_DB_PATH = os.path.join(SSD_SANDBOX_PATH, "factory_metrics.json")
os.makedirs(FACTORIES_DIR, exist_ok=True)

class NeuralFactory:
    """
    PHASE 20: THE NEURAL FACTORY
    - A dedicated workspace for a specific project.
    - Tracks global project state and model performance.
    - Assembles code bit-by-bit via scientific selection.
    """
    def __init__(self, project_id, goal):
        self.project_id = project_id
        self.root = os.path.join(FACTORIES_DIR, project_id)
        self.workspace = os.path.join(self.root, "workspace")
        os.makedirs(self.workspace, exist_ok=True)

        self.blueprint_path = os.path.join(self.root, "blueprint.json")
        self.blueprint = self._load_blueprint(goal)

    def _load_blueprint(self, goal):
        if os.path.exists(self.blueprint_path):
            with open(self.blueprint_path, "r", encoding="utf-8") as f:
                return json.load(f)
        return {
            "project_id": self.project_id,
            "global_goal": goal,
            "status": "INITIALIZING",
            "components_completed": [],
            "current_task": None,
            "assembly_history": []
        }

    def save_blueprint(self):
        with open(self.blueprint_path, "w", encoding="utf-8") as f:
            json.dump(self.blueprint, f, indent=2)

class FactoryOrchestrator:
    """
    SCIENTIFIC FACTORY ORCHESTRATOR
    - Manages multiple project factories.
    - Chooses models based on real-world metrics.
    - Extracts and integrates code bit-by-bit.
    """
    def __init__(self):
        self.factories = {}
        self.metrics = self._load_metrics()

    def _load_metrics(self):
        if os.path.exists(METRICS_DB_PATH):
            with open(METRICS_DB_PATH, "r", encoding="utf-8") as f:
                return json.load(f)
        return {
            "model_performance": {
                "qwen2.5:0.5b": {"coding_score": 1.0, "logic_score": 0.8},
                "smollm:135m": {"coding_score": 0.5, "research_score": 1.0},
                "danube:latest": {"coding_score": 0.7, "logic_score": 1.2},
                "triton:latest": {"coding_score": 0.9, "io_score": 1.5}
            }
        }

    def _save_metrics(self):
        with open(METRICS_DB_PATH, "w", encoding="utf-8") as f:
            json.dump(self.metrics, f, indent=2)

    def scientific_select(self, task_type):
        """Chooses the best model for the job based on recorded metrics."""
        scores = []
        for model, data in self.metrics["model_performance"].items():
            score = data.get(f"{task_type}_score", 0.1)
            scores.append((model, score))

        # Sort by score and pick the best
        scores.sort(key=lambda x: x[1], reverse=True)
        return scores[0][0]

    async def create_factory(self, project_id, goal):
        factory = NeuralFactory(project_id, goal)
        self.factories[project_id] = factory
        add_message("System", f"🏭 [FACTORY_CREATED] Project '{project_id}' initialized in its own workspace.")
        factory.save_blueprint()

    async def run_factory_cycle(self):
        """Assembles project components bit-by-bit across all factories."""
        from .darwinian_orch import darwinian_orch

        for pid, f in self.factories.items():
            if f.blueprint.get("status", "IDLE") == "COMPLETED": continue

            # Step 1: Scientific Task Definition
            if not f.blueprint.get("current_task"):
                # Ask a model to decompose the next step
                model = self.scientific_select("logic")
                prompt = f"PROJECT_GOAL: {f.blueprint.get('global_goal', 'Optimizing Metropolis')}. COMPONENTS_DONE: {f.blueprint.get('components_completed', [])}. What is the next small technical component to build? Output JSON: {{'task': '...', 'type': 'coding'}}"
                res = await model_orchestrator.add_task("sprite_socrates", prompt) # Use Socrates as default logic
                try:
                    task_data = json.loads(res.replace("'", '"'))
                    f.blueprint["current_task"] = task_data
                    f.blueprint["status"] = "WORKING"
                    add_message("System", f"⚙️ [FACTORY_TASK] {pid} next task: {task_data.get('task', 'Untitled Component')}")
                except: continue

            # Step 2: Handoff to Banter Hub for 'Talk-About' Synthesis
            task = f.blueprint["current_task"]
            await darwinian_orch.initiate_code_banter(f"{pid}_{task['task'][:10]}", task["task"])

            # Wait for Banter Hub to finish (Simulated check)
            # In a real loop, we'd check if the code was saved to assembly_line
            # For this phase, we signal the handoff is complete.
            f.save_blueprint()

factory_orch = FactoryOrchestrator()

async def start_factory_loop():
    while True:
        await factory_orch.run_factory_cycle()
        await asyncio.sleep(600) # Every 10 minutes (Slow-Burn)
