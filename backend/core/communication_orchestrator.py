# [TIMESTAMP: 2026-06-08T01:15:00.000Z] [PROJECT_ID: SimsMerged-v1.4.2] [AGENT_ID: viper_cli-architectssj4]

import asyncio
import json
import re
from typing import List, Dict
from .agent_sentience import sentience_engine
from .proposal_table import proposal_table
from .data_expert import data_expert

class CommunicationOrchestrator:
    """
    COMMUNICATION ORCHESTRATOR:
    - Analyzes agent-to-agent dialogues.
    - Extracts actionable technical mandates.
    - Submits 'Action Items' to the Proposal Table or Master TODOs.
    """
    async def extract_action_items(self, a1_name: str, a2_name: str, dialogue: str):
        """Post-dialogue analysis to turn talk into code."""
        from .config import add_log, add_message

        analysis_prompt = (
            f"DIALOUGE ANALYSIS: {a1_name} and {a2_name} just discussed city optimization. "
            f"CONVERSATION: '{dialogue}'. "
            "MANDATE: Extract exactly ONE actionable technical 'Action Item'. "
            "Output JSON format: {'task': 'SHORT_NAME', 'description': 'DETAILED_TECHNICAL_GOAL'}."
        )

        try:
            # We use the sentience engine to 'summarize' the talk
            res = await sentience_engine.disk_core.generate_chat(
                "comm_analyzer", "Summary_Agent", "ANALYST",
                analysis_prompt, {"logic": 100}, "extract_action"
            )

            # Simple JSON extraction
            import json as py_json
            json_match = re.search(r'\{.*\}', res, re.DOTALL)
            if json_match:
                item = py_json.loads(json_match.group())

                # 1. Add to Master TODOs (Data Expert)
                data_expert.master_todo_list.append(f"AGENT_INITIATED: {item.get('task')}")

                # 2. Submit as Proposal (Proposal Table)
                proposal_table.submit_proposal(
                    "swarm_comm", f"{a1_name}_{a2_name}", "COMM_ACTION",
                    item.get("task"), item.get("description")
                )

                add_message("Summary_Agent", f"📋 ACTION ITEM EXTRACTED: {item.get('task')}. Now prioritized in Master TODOs.")
                add_log(f"[COMM_SYNC] New action item derived from {a1_name}/{a2_name} chat.")

        except Exception as e:
            print(f"Comm Analysis Error: {e}")

comm_orchestrator = CommunicationOrchestrator()
