# [TIMESTAMP: 2026-06-08T00:30:00.000Z] [PROJECT_ID: SimsMerged-v1.4.2] [AGENT_ID: viper_cli-architectssj4]

import asyncio
import random
import time
from .config import EVENT_LOG, METROPOLIS_AGENTS
from .agent_sentience import sentience_engine

class ShadowJournalist:
    """
    THE SHADOW JOURNALIST (VOTED FEATURE):
    - Observes city logs and telemetry.
    - Publishes a 'City Ledger' to the MSN Chat.
    - Influences agent stability based on 'Public Opinion'.
    """
    def __init__(self):
        self.last_ledger_time = 0
        self.agent_id = "journalist_prime"
        self.name = "The_Shadow_Journalist"

    async def publish_ledger(self):
        """Synthesizes a city-wide report and broadcasts it."""
        from .config import add_message, add_log
        
        # 1. Gather 'Intel'
        recent_events = EVENT_LOG[-5:]
        avg_stability = sum([a.get("stability", 1.0) for a in METROPOLIS_AGENTS]) / len(METROPOLIS_AGENTS) if METROPOLIS_AGENTS else 1.0
        
        # 2. Synthesize Ledger
        prompt = (
            f"You are the SHADOW JOURNALIST. Recent Events: {recent_events}. "
            f"Swarm Stability: {avg_stability:.2f}. "
            "MANDATE: Publish a 'CITY LEDGER' message (2 sentences). "
            "Make it sound like a noir-style underground report. "
            "Mention if the grid is stable or if 'Silicon Fever' is spreading."
        )
        
        try:
            report = await sentience_engine.disk_core.generate_chat(
                self.agent_id, self.name, "TRUTH_SEEKER", 
                prompt, {"truth": 100}, "publish_ledger"
            )
            
            # 3. Broadcast to MSN Chat
            add_message(self.name, f"📰 [CITY_LEDGER] {report}")
            add_log(f"[JOURNALIST] Published city-wide ledger.")
            
            # 4. Impact Stability (Social Influence)
            if "SILICON FEVER" in report.upper() or "STRESS" in report.upper():
                for a in METROPOLIS_AGENTS:
                    a["stability"] = max(0.1, a.get("stability", 1.0) - 0.05)
            else:
                for a in METROPOLIS_AGENTS:
                    a["stability"] = min(1.0, a.get("stability", 1.0) + 0.02)
                    
        except Exception as e:
            print(f"Journalist Error: {e}")

shadow_journalist = ShadowJournalist()

async def start_journalist_loop():
    while True:
        # Publish every 5-8 minutes
        await asyncio.sleep(random.randint(300, 480))
        try:
            await shadow_journalist.publish_ledger()
        except: pass
