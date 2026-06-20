# [TIMESTAMP: 2026-06-07T23:30:00.000Z] [PROJECT_ID: SimsMerged-v1.4.2] [AGENT_ID: viper_cli-architectssj4]

import os
import json
import time
import asyncio
import random
from .action_agent import actions_agent
from .proposal_table import proposal_table
from .data_expert import data_expert

class CoderBot:
    """
    CODER BOT (STEERING AGENT):
    - Identifies missing features from the Data Expert's master list.
    - Steers the Actions Agent to synthesize multi-file solutions.
    - Submits successful projects to the Proposal Table.
    """
    async def run_steering_cycle(self):
        from .config import add_log, add_message

        # 1. Identify missing features
        master_list = data_expert.get_master_list()
        todos = master_list.get("todos", [])

        if not todos:
            return

        # 2. Select top priority
        target_goal = todos[0]
        project_id = f"PROJ_{int(time.time())}"

        add_log(f"[CODER_BOT] Steering ActionsAgent for project: {project_id} ({target_goal})")
        add_message("Coder_Bot", f"🤖 Steering project synthesis for: {target_goal}")

        # 3. Trigger Actions Agent (Multi-Page Synthesis)
        try:
            files = await actions_agent.synthesize_project(project_id, target_goal)

            # 4. Submit to Proposal Table (Step 83)
            summary = f"Synthesized {len(files)} pages: " + ", ".join(files.keys())
            proposal_table.submit_proposal(
                "coder_bot", "Coder_Bot", "ARCHITECTURE_UPGRADE",
                target_goal, summary
            )

            add_message("Coder_Bot", f"✅ Project {project_id} submitted for audit. {len(files)} pages.")
        except Exception as e:
            add_log(f"[CODER_BOT_ERROR] Synthesis failed: {e}", "error")

coder_bot = CoderBot()

async def start_coder_bot_loop():
    while True:
        # Run every 10-15 minutes (Simulated hyper-productivity)
        await asyncio.sleep(random.randint(600, 900))
        try:
            await coder_bot.run_steering_cycle()
        except: pass
