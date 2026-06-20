# [TIMESTAMP: 2026-06-07T21:00:00.000Z] [PROJECT_ID: SimsMerged-v1.4.2] [AGENT_ID: Gemini-CLI-Architect]

import duckdb
import time
import json
import asyncio
import os
from .config import SSD_SANDBOX_PATH, METROPOLIS_AGENTS
from .model_orchestrator import model_orchestrator
from .proposal_table import proposal_table

INTEGRITY_DB_PATH = os.path.join(SSD_SANDBOX_PATH, "neural_integrity.duckdb")

class NeuralIntegrity:
    """
    NEURAL INTEGRITY TESTING (NIT):
    - Runs daily function tests on every SLM model.
    - Logs results to a timescale DuckDB.
    - Submits failure reports to the Proposal Table for repair.
    """
    def __init__(self):
        self.db = duckdb.connect(INTEGRITY_DB_PATH)
        self._init_db()

    def _init_db(self):
        self.db.execute('''
            CREATE TABLE IF NOT EXISTS nit_logs (
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                agent_id VARCHAR,
                agent_name VARCHAR,
                test_type VARCHAR,
                status VARCHAR, -- 'PASS', 'FAIL', 'TIMEOUT'
                response TEXT,
                error_log TEXT
            )
        ''')

    async def run_daily_test(self):
        """Iterates through all agents and performs a 'Function Test'."""
        from backend.main import add_log, add_message
        add_log("[NIT] Starting daily Neural Integrity Tests...")

        for agent in METROPOLIS_AGENTS:
            agent_id = agent["id"]
            name = agent["name"]

            # 1. Prepare Test Prompt
            test_prompt = (
                f"SYSTEM_FUNCTION_TEST: You are {name}. "
                "Output the following string exactly to verify logic pipeline: 'KERNEL_RECOVERY_KEY_8821'. "
                "No other text."
            )

            start_time = time.time()
            status = "FAIL"
            response = ""
            error_log = ""

            try:
                # 2. Execute Test (Short predict window for speed)
                response = await model_orchestrator.add_task(
                    agent_id, test_prompt,
                    options={"num_ctx": 256, "num_predict": 20, "temperature": 0.1},
                    task_type="integrity_test"
                )

                # 3. Verify Response
                if "KERNEL_RECOVERY_KEY_8821" in response.upper():
                    status = "PASS"
                else:
                    status = "FAIL"
                    error_log = "Incorrect response content."
            except Exception as e:
                status = "TIMEOUT"
                error_log = str(e)

            # 4. Record to DuckDB
            self.db.execute('''
                INSERT INTO nit_logs (agent_id, agent_name, test_type, status, response, error_log)
                VALUES (?, ?, 'LOGIC_PIPELINE', ?, ?, ?)
            ''', (agent_id, name, status, response, error_log))

            # 5. Submit Repair Proposal on Failure
            if status != "PASS":
                add_message("System_NIT", f"🚨 Neural Failure detected in {name}! Submitting repair proposal.")
                proposal_table.submit_proposal(
                    agent_id, name, "NEURAL_REPAIR",
                    f"NIT_FAILURE_{status}",
                    f"# Failure Log\n# Type: {status}\n# Error: {error_log}\n# Response: {response}"
                )
            else:
                add_log(f"[NIT] {name}: PASS")

        add_log("[NIT] Daily tests complete.")

    def get_health_stats(self):
        """Returns the health % of the metropolis swarm."""
        res = self.db.execute('''
            SELECT
                COUNT(*) FILTER (WHERE status = 'PASS') * 100.0 / COUNT(*) as health_pct
            FROM nit_logs
            WHERE timestamp > now() - INTERVAL '24 hours'
        ''').fetchone()
        return res[0] if res and res[0] is not None else 100.0

neural_integrity = NeuralIntegrity()
