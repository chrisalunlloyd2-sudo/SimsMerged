# [TIMESTAMP: 2026-06-14T19:30:00.000Z] [PROJECT_ID: SimsMerged-v1.4.2] [AGENT_ID: viper_cli-architectssj4]
# ACTION: Layered Governance (LGA) & Judge Agent Protocol

import json
import time
import random
import asyncio
from typing import List, Dict, Optional
from .config import add_log, add_message, METROPOLIS_AGENTS
from .behavioral_scanner import behavioral_scanner

class GovernanceEngine:
    """
    METROPOLIS SUPREME COURT (LGA):
    - Audits agent code proposals and behavioral logs.
    - Implements 'Zero-Trust' verification.
    - Resolves 'Logical Disputes' between agents.
    """
    def __init__(self):
        self.laws = [
            {"id": "LAW_01", "name": "SSD Fence Integrity", "description": "No RAM caching of neural weights."},
            {"id": "LAW_02", "name": "Traceability Mandate", "description": "All code must have a valid agent signature."},
            {"id": "LAW_03", "name": "Slow-Burn Execution", "description": "Mandatory 2s jitter between tool calls."},
            {"id": "LAW_04", "name": "Zero-API Protocol", "description": "No external AI API calls allowed."}
        ]
        self.cases = []
        self.judge_agents = ["journalist_prime", "sprite_socrates"] # Specialized audit personas

    async def audit_proposal(self, agent_id: str, proposal_id: str, code: str):
        """Judge agents audit a code proposal before it's merged."""
        judge = random.choice(self.judge_agents)
        add_log(f"⚖️ [GOVERNANCE] Judge {judge} is auditing proposal {proposal_id} from {agent_id}.")
        
        # 1. LAW_04 CHECK (Zero-API)
        is_safe = "http" not in code or "localhost" in code or "127.0.0.1" in code
        
        # 2. LAW_02 CHECK (Signature)
        has_sig = "AGENT_ID" in code or "[TIMESTAMP]" in code

        verdict = "PASSED" if is_safe and has_sig else "REJECTED"
        reason = ""
        if not is_safe: reason += "Potential External API Leak detected. "
        if not has_sig: reason += "Missing Traceability Triplet. "

        case = {
            "case_id": f"CASE_{int(time.time())}",
            "defendant": agent_id,
            "judge": judge,
            "verdict": verdict,
            "reason": reason or "Compliance verified.",
            "timestamp": time.time()
        }
        self.cases.append(case)
        
        # LGA Broadcast
        from backend.tok_communications.msn_metropolis import manager
        broadcast_msg = {
            "type": "GOVERNANCE_CASE",
            "defendant": agent_id,
            "judge": judge,
            "verdict": verdict,
            "reason": case["reason"]
        }
        await manager.broadcast(json.dumps(broadcast_msg))

        # Notify via MSN
        emoji = "✅" if verdict == "PASSED" else "🚫"
        add_message(judge, f"⚖️ VERDICT: {emoji} {verdict} for {agent_id}'s proposal {proposal_id}. {reason}")
        
        return verdict == "PASSED"

    def get_legal_standing(self, agent_id: str):
        """Returns the legal standing (compliance) of an agent."""
        agent_cases = [c for c in self.cases if c["defendant"] == agent_id]
        if not agent_cases: return 1.0
        passed = len([c for c in agent_cases if c["verdict"] == "PASSED"])
        return passed / len(agent_cases)

governance_engine = GovernanceEngine()
