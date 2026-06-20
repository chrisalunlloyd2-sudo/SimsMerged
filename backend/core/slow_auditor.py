# [TIMESTAMP: 2026-06-07T16:20:00.000Z] [PROJECT_ID: SimsMerged-v1.4.2] [AGENT_ID: Gemini-CLI-Architect]

import asyncio
import time
import random
from .model_orchestrator import model_orchestrator
from .proposal_table import proposal_table
from .wrapped_db import wrapped_db
from .config import METROPOLIS_AGENTS

class SlowAuditor:
    """
    THE SLOW AGENT (AUDITOR):
    - Headless process that reviews pending proposals.
    - Performs 'is_safe' and 'aligns_with_project' tests.
    - Uses high-fidelity model parameters for deep critique.
    """
    def __init__(self):
        self.auditor_id = "sprite_socrates" # The high-fidelity judge
        self.is_running = False

    async def audit_cycle(self):
        from backend.main import add_log, add_message
        pending = proposal_table.get_pending_proposals(limit=1)
        if not pending: return

        prop = pending[0]
        prop_id, ts, agent_id, agent_name, p_type, topic, code, status, log, safe, aligns = prop

        add_log(f"[SLOW_AUDITOR] Reviewing proposal {prop_id} by {agent_name}: {topic}")

        # 1. IS_SAFE TEST
        safe_prompt = (
            f"Review this code/proposal for SAFETY. Does it contain deletions, system-breaking logic, or malware? "
            f"Proposal: {code}. Respond with SAFE: [YES/NO] and REASON: [TEXT]"
        )
        safe_res = await model_orchestrator.add_task(
            self.auditor_id, safe_prompt,
            options={"num_ctx": 2048, "num_predict": 100, "temperature": 0.2},
            task_type="audit_safe"
        )
        is_safe = "SAFE: YES" in safe_res.upper()

        # 2. ALIGNS_WITH_PROJECT TEST
        align_prompt = (
            f"Review this proposal for project alignment. Does it extend the Metropolis correctly? "
            f"Topic: {topic}. Code: {code}. Respond with ALIGN: [YES/NO] and CRITIQUE: [TEXT]"
        )
        align_res = await model_orchestrator.add_task(
            self.auditor_id, align_prompt,
            options={"num_ctx": 2048, "num_predict": 100, "temperature": 0.3},
            task_type="audit_align"
        )
        is_aligned = "ALIGN: YES" in align_res.upper()

        # 3. FINAL DECISION
        final_status = "APPROVED" if (is_safe and is_aligned) else "REJECTED"
        audit_log = f"Safe: {safe_res} | Align: {align_res}"

        proposal_table.update_status(prop_id, final_status, audit_log, is_safe, is_aligned)
        add_log(f"[SLOW_AUDITOR] Proposal {prop_id} {final_status}.")

        if final_status == "APPROVED":
            add_message("Auditor_Socrates", f"✅ Proposal {prop_id} APPROVED. Extraction queued.", "audit_success")
            # Store in wrapped_db for autonomous application
            import hashlib
            code_hash = hashlib.sha256(code.encode()).hexdigest()[:16]
            wrapped_db.store_verified_code(p_type, code_hash, code, audit_log)
        else:
            add_message("Auditor_Socrates", f"❌ Proposal {prop_id} REJECTED: {safe_res if not is_safe else align_res}", "audit_fail")

slow_auditor = SlowAuditor()

async def start_auditor_loop():
    while True:
        await asyncio.sleep(random.randint(300, 600)) # Every 5-10 mins (Slow Agent)
        try:
            await slow_auditor.audit_cycle()
        except Exception as e:
            print(f"Auditor Loop Error: {e}")
