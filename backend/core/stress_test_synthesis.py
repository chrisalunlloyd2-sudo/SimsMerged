# [TIMESTAMP: 2026-06-14T13:15:00.000Z] [PROJECT_ID: SimsMerged-v1.4.2] [AGENT_ID: viper_cli-architectssj4]

import asyncio
import os
import sys

# Path setup
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from backend.core.research_synthesis import synthesis_engine
from backend.core.validation_agent import validate_research_paper
from backend.core.process_manager import process_manager
from backend.core.config import add_log, add_message

async def run_stress_test():
    topic = "The Evolutionary Taxonomy and Genetic Divergence of Felis Catus in Urban Metropolis Environments"
    add_log(f"🚀 [STRESS_TEST] Initiating Phase 9 Stress Test for topic: {topic}")

    attempts = 0
    max_attempts = 3

    while attempts < max_attempts:
        attempts += 1
        add_log(f"📝 [STRESS_TEST] Attempt {attempts}/{max_attempts}")

        # Step 27: Clean Slate
        zombies = process_manager.cleanup_zombies()
        if zombies > 0:
            add_log(f"🧹 [STRESS_TEST] Cleaned up {zombies} zombie processes.")

        try:
            # Step 22: Execute Synthesis Loop
            file_path = await synthesis_engine.generate_comprehensive_paper(topic)

            # Step 24: Validate word count (>17,500 words)
            if validate_research_paper(file_path):
                add_log(f"✅ [STRESS_TEST] SUCCESS! Paper validated at {file_path}")
                add_message("System", f"🏆 Phase 9 Stress Test passed on attempt {attempts}.")
                return True
            else:
                add_log(f"❌ [STRESS_TEST] FAILED: Paper did not meet fidelity requirements.", level="warning")
        except Exception as e:
            add_log(f"💥 [STRESS_TEST] ERROR during synthesis: {e}", level="error")

        await asyncio.sleep(10) # Cooling down before retry

    add_log("💀 [STRESS_TEST] ABORTED: Failed to reach 35-page finality after 3 attempts.", level="critical")
    return False

if __name__ == "__main__":
    asyncio.run(run_stress_test())
