# [TIMESTAMP: 2026-06-14T19:10:00.000Z] [PROJECT_ID: SimsMerged-v1.4.2] [AGENT_ID: viper_cli-architectssj4]
# ACTION: Automated Agent Test Suite & Pattern Invention Pipeline

import pytest
import os
import json
import asyncio
from backend.core.config import SSD_SANDBOX_PATH
from backend.core.action_agent import actions_agent
from backend.core.pattern_recognition import pattern_engine

# The directory where agents will write and run tests against their own logic
TEST_SANDBOX = os.path.join(SSD_SANDBOX_PATH, "autonomous_tests")
os.makedirs(TEST_SANDBOX, exist_ok=True)

class TestSovereignty:
    """
    Manages the lifecycle of agent-written tests.
    Agents propose new logic (patterns), write a test, run the test,
    and if it passes, the pattern is committed to the Pattern Engine.
    """
    def __init__(self):
        self.active_inventions = {}

    async def propose_invention(self, agent_id: str, concept: str, logic_code: str, test_code: str):
        """Agents submit a new invention here."""
        invention_id = f"inv_{agent_id}_{int(asyncio.get_event_loop().time())}"

        # Save logic
        logic_path = os.path.join(TEST_SANDBOX, f"{invention_id}_logic.py")
        with open(logic_path, "w") as f:
            f.write(logic_code)

        # Save test
        test_path = os.path.join(TEST_SANDBOX, f"test_{invention_id}.py")
        # Ensure test imports the logic correctly
        test_content = f"import sys\nsys.path.append(r'{TEST_SANDBOX}')\nimport {invention_id}_logic\n\n{test_code}"
        with open(test_path, "w") as f:
            f.write(test_content)

        self.active_inventions[invention_id] = {
            "agent_id": agent_id,
            "concept": concept,
            "logic_path": logic_path,
            "test_path": test_path,
            "status": "PENDING_EXECUTION"
        }
        return invention_id

    async def execute_test(self, invention_id: str):
        """Runs pytest on the agent's submitted test file."""
        if invention_id not in self.active_inventions:
            return {"status": "error", "message": "Invention not found."}

        inv = self.active_inventions[invention_id]

        # LGA Mandate: Governance Audit
        from backend.core.governance import governance_engine
        with open(inv["logic_path"], "r") as f:
            logic_content = f.read()

        # Update agent status to SYNTHESIZING for visual particles
        from backend.tok_communications.msn_metropolis import manager
        await manager.broadcast(json.dumps({"type": "AGENT_UPDATE", "agent_id": inv["agent_id"], "status": "SYNTHESIZING"}))

        is_legal = await governance_engine.audit_proposal(inv["agent_id"], invention_id, logic_content)
        if not is_legal:
            inv["status"] = "REJECTED_BY_GOVERNANCE"
            return {"status": "rejected", "message": "Invention rejected by Layered Governance (LGA) Audit."}

        test_path = inv["test_path"]

        # Run pytest programmatically or via subprocess
        import subprocess
        # Using stealth execution principles (throttle, isolation)
        cmd = f'C:\\Users\\viper\\python\\python.exe -m pytest "{test_path}" -v --tb=short'

        try:
            process = await asyncio.create_subprocess_shell(
                cmd,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )
            stdout, stderr = await process.communicate()
            exit_code = process.returncode

            if exit_code == 0:
                inv["status"] = "PASSED"
                # Register the successful pattern!
                with open(inv["logic_path"], "r") as f:
                    logic_content = f.read()

                # 1. Store in DuckDB Action DB for reuse
                actions_agent.record_success("python", inv["concept"], logic_content, {"agent": inv["agent_id"], "type": "invention"})

                # 2. Store in Logit DB for geometric mapping
                pattern_engine.store_pattern(invention_id, "AGENT_INVENTION", logic_content, {"agent": inv["agent_id"], "concept": inv["concept"]})

                return {"status": "success", "message": "Test passed. Pattern Integrated.", "output": stdout.decode()}
            else:
                inv["status"] = "FAILED"
                return {"status": "failed", "message": "Test failed.", "output": stdout.decode() + stderr.decode()}

        except Exception as e:
            inv["status"] = "ERROR"
            return {"status": "error", "message": str(e)}

test_sovereignty = TestSovereignty()
