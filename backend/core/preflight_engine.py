# [TIMESTAMP: 2026-06-11T05:30:00.000Z] [PROJECT_ID: SimsMerged-v1.4.2] [AGENT_ID: Gemini-CLI-Architect]

import asyncio
import time
import random
import os
import json
from .config import SSD_SANDBOX_PATH, add_log, add_message, METROPOLIS_AGENTS
from .model_orchestrator import model_orchestrator
from .evolution_council import evolution_council
from .qwen_ide import qwen_ide
from .wisdom_tree import wisdom_tree

class PreflightEngine:
    """
    THE PREFLIGHT ENGINE (PHASE 35):
    - Executes 50-100 iterative testing & voting cycles.
    - Manages the 'Genetic Darwin' prompt enhancement loop.
    - Coordinates the swarm to build and verify coding combinations.
    """
    def __init__(self):
        self.iteration = 0
        self.max_iterations = 100
        self.findings_file = os.path.join(SSD_SANDBOX_PATH, "swarm_findings.json")
        self.genetic_prompt_file = os.path.join(SSD_SANDBOX_PATH, "genetic_prompts.json")
        self.gui_goals = [
            "Implement Save Simulation State (Backend + Java)",
            "Create Resource Quotas View in JavaFX",
            "Add Minimap Visibility Toggle logic",
            "Implement Treasury Ledger Auto-Refresh",
            "Build AI Agent Relationship Graph Component"
        ]
        self._init_genetic_prompts()

    def _init_genetic_prompts(self):
        if not os.path.exists(self.genetic_prompt_file):
            default_prompts = {
                "GUI_FIX": "Analyze the JavaFX source code and identify a visual bottleneck or missing component. Propose a specific 'JavaFX Neo' implementation.",
                "BACKEND_FIX": "Analyze the FastAPI backend and identify a potential logic collision in agent synchronization. Propose a thread-safe solution.",
                "PREFLIGHT_TEST": "Design a 'Preflight' testing wrapper that validates the consensus of 4 agents on a technical mandate.",
                "GUI_GOAL": "Target a specific GUI goal: {goal}. Design the JavaFX architecture and backend endpoint required."
            }
            with open(self.genetic_prompt_file, "w") as f:
                json.dump(default_prompts, f, indent=2)

    async def get_evolved_prompt(self, category, goal=None):
        with open(self.genetic_prompt_file, "r") as f:
            prompts = json.load(f)
        p = prompts.get(category, "Perform a technical optimization.")
        if goal:
            p = p.replace("{goal}", goal)
        return p

    async def mutate_prompt(self, category, critique):
        """Darwinian Mutation: Updates the prompt based on failed or successful iterations."""
        add_message("Genetic_Mutator", f"🧬 [MUTATION] Enhancing the '{category}' prompt based on swarm critique.")
        with open(self.genetic_prompt_file, "r") as f:
            prompts = json.load(f)

        current_prompt = prompts[category]
        mutation_prompt = (
            f"GENETIC_MUTATOR: We are in the Preflight phase. Current Prompt: '{current_prompt}'. "
            f"Critique from swarm: '{critique}'. "
            "Rewrite the prompt to be more technical, specific, and effective for a local SLM. "
            "Output ONLY the new prompt string."
        )

        try:
            new_prompt = await model_orchestrator.add_task("sprite_writer", mutation_prompt, task_type="genetic_mutation")
            prompts[category] = new_prompt
            with open(self.genetic_prompt_file, "w") as f:
                json.dump(prompts, f, indent=2)
            add_log(f"🧬 [GENETIC_EVOLUTION] {category} prompt mutated.")
        except: pass

    async def run_preflight_cycle(self):
        """The core 100-iteration loop (PHASE 35)."""
        timestamp = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
        add_log(f"[{timestamp}] [SimsMerged-v1.4.2] [Preflight_Engine] 🛫 Initiating 100-iteration batch.")

        while self.iteration < self.max_iterations:
            self.iteration += 1
            it_start_time = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
            add_message("System", f"🔄 [{it_start_time}] [SimsMerged-v1.4.2] [PREFLIGHT_ITERATION {self.iteration}/{self.max_iterations}] Initiating cycle...")

            # 1. HYPOTHESIS PHASE
            category = random.choice(["GUI_FIX", "BACKEND_FIX", "PREFLIGHT_TEST", "GUI_GOAL"])
            goal = random.choice(self.gui_goals) if category == "GUI_GOAL" else None
            evolved_prompt = await self.get_evolved_prompt(category, goal=goal)

            proposer = random.choice(METROPOLIS_AGENTS)
            hypothesis = await model_orchestrator.add_task(proposer["id"], evolved_prompt, task_type="hypothesis")
            add_message(proposer["name"], f"💡 [HYPOTHESIS] {hypothesis[:200]}...")

            # 2. CRITIQUE PHASE
            critic = random.choice(METROPOLIS_AGENTS)
            while critic["id"] == proposer["id"]: critic = random.choice(METROPOLIS_AGENTS)

            critique_prompt = f"TECHNICAL CRITIQUE: Analyze this hypothesis from {proposer['name']}: '{hypothesis}'. Identify any logical flaws or SSD I/O risks."
            critique = await model_orchestrator.add_task(critic["id"], critique_prompt, task_type="critique")
            add_message(critic["name"], f"🧐 [CRITIQUE] {critique[:200]}...")

            # 3. VOTE PHASE
            crawl_data = {"topic": f"Preflight_{category}_{self.iteration}", "hash": f"it_{self.iteration}"}
            approved = await evolution_council.execute_vote(crawl_data)

            # 4. EXECUTE & RECORD
            if approved:
                add_message("System", "🗳️ [VOTE_PASSED] Executing coding combination...")
                task_id = await qwen_ide.propose_coding_task(f"Preflight_{category}", hypothesis)

                # Perform 1 iteration of the IDE cycle immediately
                await qwen_ide.run_slow_burn_cycle()

                # Record the finding
                model_orchestrator.record_finding(proposer["id"], f"Iteration {self.iteration} Passed", hypothesis)
            else:
                add_message("System", "🗳️ [VOTE_REJECTED] Cycle discarded. Initiating Genetic Mutation.")
                await self.mutate_prompt(category, critique)

            # Iteration cooldown (Slow-Burn)
            await asyncio.sleep(60)

preflight_engine = PreflightEngine()

async def start_preflight_loop():
    await preflight_engine.run_preflight_cycle()
