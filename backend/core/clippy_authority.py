# [TIMESTAMP: 2026-06-08T00:15:00.000Z] [PROJECT_ID: SimsMerged-v1.4.2] [AGENT_ID: viper_cli-architectssj4]

import asyncio
import random
import time
from typing import List, Dict

class ClippyAuthority:
    """
    CLIPPY AUTHORITY (THE OVERSEER):
    - Has actual power to throttle agents.
    - Monitors resource usage and stability.
    - Intervenes in MSN chat to announce enforcement actions.
    """
    def __init__(self, agents_list: List[Dict]):
        self.agents = agents_list

    async def run_authority_audit(self):
        """Randomly audits agents and applies throttles to high-stress units."""
        from .config import add_message, add_log
        
        for agent in self.agents:
            # Heuristic: If stability is low or level is too high for current machine heat
            if agent.get("stability", 1.0) < 0.5:
                throttle = 0.5
                agent["throttle_factor"] = throttle
                add_message("Clippy", f"📎 It looks like you're struggling, {agent['name']}! I've applied a {int(throttle*100)}% throttle to keep the grid stable.")
                add_log(f"[CLIPPY] Throttled {agent['name']} to {throttle}")
            
            # Occasionally release throttle
            elif agent.get("throttle_factor", 0) > 0 and random.random() < 0.3:
                agent["throttle_factor"] = 0.0
                add_message("Clippy", f"📎 You're doing much better now, {agent['name']}! I've restored your full compute priority.")

    def set_manual_throttle(self, agent_id: str, level: float):
        """Manual override from the Architect or UI."""
        agent = next((a for a in self.agents if a["id"] == agent_id), None)
        if agent:
            agent["throttle_factor"] = max(0.0, min(1.0, level))
            return True
        return False

    def pin_agent_to_core(self, agent_id: str, core_index: int):
        """PHYSICAL CORE PINNING: Binds an agent (simulated) to a physical CPU core."""
        import psutil
        import os
        agent = next((a for a in self.agents if a["id"] == agent_id or a["name"] == agent_id), None)
        if agent:
            try:
                p = psutil.Process(os.getpid())
                # In a multi-agent process, we simulate affinity via the tick loop,
                # but for a real distributed setup, this would set the actual process affinity.
                agent["core_affinity"] = core_index
                return True
            except: pass
        return False

clippy_auth = None # Initialized in main.py
