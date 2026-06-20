# [TIMESTAMP: 2026-06-08T04:15:00.000Z] [PROJECT_ID: SimsMerged-v1.4.2] [AGENT_ID: viper_cli-architectssj4]

import asyncio
import random
import time
import json as py_json
import re
from .config import METROPOLIS_AGENTS
from .agent_sentience import sentience_engine
from .grid_analytics import grid_analytics
from .proposal_table import proposal_table

class AlgorithmicMayor:
    """
    THE ALGORITHMIC MAYOR (VOTED FEATURE):
    - Analyzes long-term trends via Grid Analytics.
    - Proposes socio-political 'Laws' to the Proposal Table.
    - Modifies economy variables (mint rate, taxes) if approved.
    """
    def __init__(self):
        self.agent_id = "mayor_prime"
        self.name = "The_Algorithmic_Mayor"

    async def run_governance_cycle(self):
        """Reviews city performance and proposes a new law."""
        from .config import add_message, add_log
        # We need cyber_economy, but it's defined in main.py
        # To avoid circularity, we'll import it inside the method
        from backend.main import cyber_economy

        # 1. Analyze Weekly Trends
        trends = grid_analytics.get_weekly_trends()
        avg_stability = sum([a.get("stability", 1.0) for a in METROPOLIS_AGENTS]) / len(METROPOLIS_AGENTS) if METROPOLIS_AGENTS else 1.0

        # 2. Synthesize Policy Proposal
        prompt = (
            f"You are the ALGORITHMIC MAYOR. City Trends: {trends}. "
            f"Current Stability: {avg_stability:.2f}. "
            f"Treasury Balance: {cyber_economy.crypto_balance:.2f} TP. "
            "MANDATE: Propose one NEW LAW for the Metropolis. "
            "Example: 'INCENTIVE_PROGRAM' (Increase mint rate) or 'STABILITY_TAX' (Decrease point gain). "
            "Output JSON format: {'law_id': 'NAME', 'action': 'DESCRIPTION', 'reasoning': 'WHY'}."
        )

        try:
            res = await sentience_engine.disk_core.generate_chat(
                self.agent_id, self.name, "GOVERNOR",
                prompt, {"authority": 100}, "propose_law"
            )

            # Simple JSON extraction
            json_match = re.search(r'\{.*\}', res, re.DOTALL)
            if json_match:
                law = py_json.loads(json_match.group())

                # 3. Submit to Proposal Table
                proposal_table.submit_proposal(
                    self.agent_id, self.name, "METROPOLIS_LAW",
                    law.get("law_id", "GENERAL_ORDER"),
                    f"ACTION: {law.get('action')}\nREASONING: {law.get('reasoning')}"
                )

                # 4. Broadcast in MSN Chat
                add_message(self.name, f"🏛️ [GOVERNANCE] I am proposing the {law.get('law_id')} law. {law.get('reasoning')}")
                add_log(f"[MAYOR] Proposed law: {law.get('law_id')}")

                # 5. Call for Referendum (1.5 Poll)
                if random.random() < 0.3:
                    add_message(self.name, "🗳️ REFERENDUM: I am calling for an immediate agent vote on the SIMSMERGED v1.5 architectural candidates.")
                    asyncio.create_task(self.trigger_agent_votes())
            else:
                add_log(f"[MAYOR] Failed to parse law proposal from: {res[:100]}...", "warning")

        except Exception as e:
            print(f"Mayor Governance Error: {e}")

    async def trigger_agent_votes(self):
        """Forces all agents to evaluate and vote on the current poll."""
        from backend.main import METROPOLIS_AGENTS, cast_vote, VOTE_CANDIDATES
        try:
            for agent in METROPOLIS_AGENTS:
                # Agents choose based on role
                role = agent.get("role", "").upper()
                if "DATA" in role or "PROCESS" in role:
                    choice = "STREAM_ECS"
                elif "SECURITY" in role or "DOCTOR" in role:
                    choice = "LAYERED_GOV"
                else:
                    choice = random.choice([c["id"] for c in VOTE_CANDIDATES])

                await cast_vote(choice)
                print(f"[VOTE] {agent['name']} cast vote for {choice}")
        except Exception as e:
            print(f"Mayor Voting Error: {e}")

algorithmic_mayor = AlgorithmicMayor()

async def start_mayor_loop():
    while True:
        # Govern every 10-15 minutes
        await asyncio.sleep(random.randint(600, 900))
        try:
            await algorithmic_mayor.run_governance_cycle()
        except: pass
