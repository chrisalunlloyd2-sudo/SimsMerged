import asyncio
import time
import json
import os
import traceback
import sys
import importlib
from .agent_registrar import update_agents

# Memory for infinite learning
LEARNING_LEDGER = "orchestrator_learning_ledger.json"

class SelfHealingOrchestrator:
    def __init__(self):
        self.generation = 1
        self.health = 1.0
        self.learning_rate = 0.01
        self.weights = {"agent_sync_speed": 1.2, "healing_factor": 0.05, "error_count": 0}
        self.load_learning()
        print(f"[ORCHESTRATOR] Genesis v{self.generation} Online. Weights: {self.weights}")

    def load_learning(self):
        """Infinite learning loop state persistence"""
        try:
            if os.path.exists(LEARNING_LEDGER):
                with open(LEARNING_LEDGER, "r") as f:
                    data = json.load(f)
                    self.generation = data.get("generation", 1) + 1
                    self.weights = data.get("weights", self.weights)
        except Exception:
            pass

    def save_learning(self):
        try:
            with open(LEARNING_LEDGER, "w") as f:
                json.dump({"generation": self.generation, "weights": self.weights, "last_updated": time.time()}, f, indent=2)
        except Exception:
            pass

    def self_modify(self):
        """Dynamically adjusts its own operational weights based on health metrics"""
        if self.health < 0.8:
            print("[ORCHESTRATOR] Health degraded. Modifying operational weights to heal.")
            self.weights["agent_sync_speed"] = min(10.0, self.weights["agent_sync_speed"] * 1.5) # Slow down sync to save CPU
            self.weights["healing_factor"] *= 1.1 # Increase healing priority
            self.health += self.weights["healing_factor"]
            self.health = min(1.0, self.health)
        else:
            # Continually optimize for speed if healthy, but maintain a floor to prevent IO saturating
            self.weights["agent_sync_speed"] = max(2.0, self.weights["agent_sync_speed"] * 0.99)

        # Optimization: Only save learning every 300 seconds (5 mins) instead of every loop
        if time.time() - self.weights.get("last_save", 0) > 300:
            self.weights["last_save"] = time.time()
            self.save_learning()

    async def run_forever(self):
        while True:
            try:
                # Core operational logic
                start_time = time.time()

                update_agents()

                with open("../PULSE_HEARTBEAT.txt", "w") as f:
                    f.write(str(time.time()))

                # Infinite Learning Step
                self.self_modify()

                sync_delay = self.weights.get("agent_sync_speed", 1.2)
                await asyncio.sleep(sync_delay)

            except Exception as e:
                # Self-Healing Step
                self.weights["error_count"] = self.weights.get("error_count", 0) + 1
                print(f"[CRITICAL_ERROR] Orchestrator crashed: {e}. Initiating self-healing sequence...")
                traceback.print_exc()
                self.health -= 0.2
                self.self_modify()
                print(f"[ORCHESTRATOR] Self-healing complete. System health: {self.health:.2f}. Restarting main loop.")
                await asyncio.sleep(2.0)

async def start_orchestrator():
    orchestrator = SelfHealingOrchestrator()
    await orchestrator.run_forever()