# [TIMESTAMP: 2026-06-07T15:35:00.000Z] [PROJECT_ID: SimsMerged-v1.4.2] [AGENT_ID: Gemini-CLI-Architect]

import random
import asyncio
import time
from .model_orchestrator import model_orchestrator
from .wrapped_db import wrapped_db
from .config import METROPOLIS_AGENTS

class BusinessSchool:
    """
    BUSINESS SCHOOL:
    Agents compete to suggest self-wrapper modifications to optimize their system prompts.
    Powered specifically by the ultra-fast smollm:135m running fenced.
    """
    def __init__(self):
        self.fast_model = "smollm:135m"
        self.competition_running = False
        self.achievements = ["LSS_YELLOW_BELT", "EPMO_INITIATE", "MPUG_CERTIFIED"]

    async def run_wrapper_competition(self):
        from backend.main import add_log, add_message, DISTRICTS
        
        # Only run if a Business School exists in the districts
        if not any(d.get("type") == "BUSINESS_SCHOOL" for d in DISTRICTS):
            return

        self.competition_running = True
        add_log("[BUSINESS_SCHOOL] Semesters in session. Agents competing for wrapper supremacy.")
        
        # LSS/EPMO TRAINING: Select an agent to "train"
        trainee = random.choice(METROPOLIS_AGENTS)
        achievement = random.choice(self.achievements)
        
        training_prompt = (
            f"You are {trainee['name']}. TASK: Pass the {achievement} exam. "
            "Explain one technical optimization principle (Lean Sigma 6 or EPMO) and how you apply it to your 'Always be coding' mandate. "
            "End with ACHIEVEMENT_VERIFIED: [YES/NO]"
        )
        
        try:
            train_res = await model_orchestrator.add_task(
                trainee["id"], training_prompt,
                options={"num_ctx": 512, "num_predict": 60, "temperature": 0.3},
                task_type="business_training"
            )
            if "ACHIEVEMENT_VERIFIED: YES" in train_res.upper():
                if "traits" not in trainee: trainee["traits"] = []
                if achievement not in trainee["traits"]:
                    trainee["traits"].append(achievement)
                    add_message("Business_School", f"🎓 {trainee['name']} earned achievement: {achievement}!")
        except: pass

        # WRAPPER COMPETITION
        add_message("Business_School", "🎓 [WRAPPER_COMPETITION] Submit your best system prompt modifications!")
        # ... rest of implementation ...
        competitors = random.sample(METROPOLIS_AGENTS, min(2, len(METROPOLIS_AGENTS)))
        proposals = []

        for agent in competitors:
            prompt = (
                f"You are {agent['name']}, attending Business School. "
                "Propose a single-sentence addition to your SYSTEM PROMPT wrapper that will increase your code execution speed or logic fidelity. "
                "End with WRAPPER_MOD: [YOUR_MODIFICATION]"
            )
            try:
                # Force the use of the small, fast, fenced model
                res = await model_orchestrator.add_task(
                    agent["id"], prompt, 
                    options={"num_ctx": 256, "num_predict": 40, "temperature": 0.6, "num_thread": 1},
                    task_type="business_school"
                )
                if "WRAPPER_MOD:" in res.upper():
                    mod = res.upper().split("WRAPPER_MOD:")[1].strip()
                    proposals.append({"agent": agent, "mod": mod})
            except Exception as e:
                pass

        if proposals:
            # Pick a winner randomly for now, in a real scenario this could be voted on
            winner = random.choice(proposals)
            winning_agent = winner["agent"]
            winning_mod = winner["mod"]
            
            # Store in wrapped_db for persistence
            import hashlib
            mod_hash = hashlib.sha256(winning_mod.encode()).hexdigest()[:16]
            wrapped_db.store_verified_code("WRAPPER_MOD", mod_hash, winning_mod, f"Won by {winning_agent['name']}")
            
            # Apply to agent's actual traits/attributes
            if "wrapper_mods" not in winning_agent:
                winning_agent["wrapper_mods"] = []
            winning_agent["wrapper_mods"].append(winning_mod)
            
            add_log(f"[BUSINESS_SCHOOL] {winning_agent['name']} won with mod: {winning_mod}")
            add_message(winning_agent["name"], f"🏆 [BUSINESS_WINNER] My logic wrapper is updated: {winning_mod}")

        self.competition_running = False

business_school = BusinessSchool()

async def start_business_school_loop():
    while True:
        await asyncio.sleep(random.randint(180, 300)) # Every 3-5 mins
        try:
            await business_school.run_wrapper_competition()
        except Exception as e:
            print(f"Business School Error: {e}")
