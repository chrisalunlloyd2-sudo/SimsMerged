# [TIMESTAMP: 2026-06-08T08:45:00.000Z] [PROJECT_ID: SimsMerged-v1.4.2] [AGENT_ID: viper_cli-architectssj4]

import os
import json
import random
import time
import asyncio
import re
from typing import List, Dict
from .config import SSD_SANDBOX_PATH, add_log, add_message
from .model_orchestrator import model_orchestrator
from .execution_engine import execution_sandbox
from .wisdom_tree import wisdom_tree

PROMPT_GENETICS_PATH = os.path.join(SSD_SANDBOX_PATH, "prompt_genetics.json")

class DarwinianOrchestrator:
    """
    PHASE 19: THE TALK-ABOUT METHOD
    - Agents bounce ideas in chat (Banter Hub).
    - Orchestrator extracts code from consensus.
    - Genetically advances system prompts based on success.
    - Implements the 10-fail rephrase rule.
    """
    def __init__(self):
        self.genetics = self._load_genetics()
        self.active_debates = {} # project_name -> {history, fail_count, round}
        
    def _load_genetics(self):
        if os.path.exists(PROMPT_GENETICS_PATH):
            with open(PROMPT_GENETICS_PATH, "r", encoding="utf-8") as f:
                return json.load(f)
        return {
            "sprite_geek": {"dna": "You are a technical coder. Be concise.", "fitness": 1.0},
            "sprite_writer": {"dna": "You are a logic researcher.", "fitness": 1.0},
            "sprite_socrates": {"dna": "You are a critical logic gate.", "fitness": 1.0}
        }

    def _save_genetics(self):
        with open(PROMPT_GENETICS_PATH, "w", encoding="utf-8") as f:
            json.dump(self.genetics, f, indent=2)

    async def evolve_prompt(self, agent_id, success: bool):
        """Darwinian Evolution: Mutate system prompts based on outcome."""
        gene = self.genetics.get(agent_id)
        if not gene: return
        
        if success:
            gene["fitness"] += 0.1
        else:
            gene["fitness"] -= 0.05
            # Mutation Phase
            mutations = [
                " Use more technical jargon.",
                " Focus on zero-copy optimizations.",
                " Prioritize hardware-level stability.",
                " Be extremely verbose about logic flows.",
                " Think in recursive patterns."
            ]
            if random.random() < 0.3:
                gene["dna"] += random.choice(mutations)
        
        self._save_genetics()

    async def initiate_code_banter(self, project_name, goal):
        """Start the 'Talk-About' session in MSN Chat."""
        self.active_debates[project_name] = {
            "goal": goal,
            "history": [],
            "fail_count": 0,
            "round": 0,
            "status": "TALKING"
        }
        add_message("System", f"🗣️ [BANTER_HUB] Initiating Darwinian debate for: {project_name}")

    async def process_banter_cycle(self):
        """The non-stop circle of agents talking about the code."""
        for name, d in list(self.active_debates.items()):
            if d["status"] != "TALKING": continue
            
            d["round"] += 1
            if d["round"] > 50:
                add_message("System", f"🛑 [ENGINEERING_LIMIT] Project {name} reached 50 rounds. Archiving.")
                del self.active_debates[name]
                continue

            # 1. Bouncing Ideas
            agents = ["sprite_writer", "sprite_geek", "sprite_socrates"]
            speaker = agents[(d["round"] - 1) % 3]
            
            dna = self.genetics[speaker]["dna"]
            prompt = (
                f"{dna} We are talking about building: {d['goal']}. "
                f"Previous thoughts: {json.dumps(d['history'][-2:])}. "
                "What is the next technical step or code block? Bounce your idea to the next agent."
            )
            
            try:
                thought = await model_orchestrator.add_task(speaker, prompt, task_type="code_banter")
                d["history"].append(f"{speaker}: {thought}")
                add_message(speaker, f"🗨️ [TALK_ABOUT] {thought}")
                
                # 2. Grab Code if Consensus reached (heuristically checking for code blocks)
                if "```" in thought or "def " in thought or "import " in thought:
                    await self._try_extract_and_test(name, thought, speaker)
                    
            except Exception as e:
                add_log(f"[BANTER_ERR] {e}", "error")

    async def _try_extract_and_test(self, project_name, content, agent_id):
        """The Logic Gate: Grabs the code from chat and tests it."""
        d = self.active_debates[project_name]
        
        # Regex to pull code from banter
        code_match = re.search(r"```(?:python)?(.*?)```", content, re.DOTALL)
        code = code_match.group(1).strip() if code_match else content
        
        # FACTORY AWARENESS: Check if this project is part of a Neural Factory
        from .factory_orch import factory_orch
        factory_id = None
        if "_" in project_name:
            potential_fid = project_name.split("_")[0]
            if potential_fid in factory_orch.factories:
                factory_id = potential_fid

        filename = f"banter_{project_name.lower().replace(' ', '_')}.py"
        
        if factory_id:
            dest_dir = factory_orch.factories[factory_id].workspace
            filepath = os.path.join(dest_dir, filename)
        else:
            filepath = os.path.join(SSD_SANDBOX_PATH, "assembly_line", filename)
        
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(code)
            
        # Predictive Testing (Execution)
        result = execution_sandbox.run_script(filename)
        
        if "SUCCESS" in result:
            add_message("System", f"✅ [BANTER_WIN] Code for {project_name} verified. Integrated into workspace.")
            await self.evolve_prompt(agent_id, True)
            wisdom_tree.store_wisdom(project_name, code)
            
            # Update Factory Blueprint if applicable
            if factory_id:
                factory = factory_orch.factories[factory_id]
                factory.blueprint["components_completed"].append(project_name)
                factory.blueprint["current_task"] = None
                factory.blueprint["assembly_history"].append({"task": project_name, "code_hash": hashlib.sha256(code.encode()).hexdigest()[:8]})
                factory.save_blueprint()
                
            del self.active_debates[project_name]
        else:
            d["fail_count"] += 1
            await self.evolve_prompt(agent_id, False)
            add_message("Judge_Socrates", f"🟥 [BANTER_FAIL] Attempt {d['fail_count']}/10. Error: {result[:50]}...")
            
            if d["fail_count"] >= 10:
                add_message("System", f"🔄 [REPHRASE_MANDATE] 10 fails reached. Re-formatting performative for {project_name}...")
                d["goal"] = f"REPHRASED: Implement {d['goal']} using a different architectural pattern."
                d["fail_count"] = 0 # Reset for new round

darwinian_orch = DarwinianOrchestrator()

async def start_banter_loop():
    while True:
        await darwinian_orch.process_banter_cycle()
        await asyncio.sleep(5) # Paced for 'Slow-Burn' visibility
