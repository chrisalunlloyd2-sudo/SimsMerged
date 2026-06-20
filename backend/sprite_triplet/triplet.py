# TIMESTAMP: 2026-06-09
# PROJECT_ID: SimsMerged-v1.4.2
# AGENT_ID: viper_cli-architectssj4
# DESCRIPTION: Industrial Cascading logic with Role Sharding and Intent Prefixes

import asyncio
import httpx
import logging
from .config import TripletConfig

logger = logging.getLogger("SpriteTriplet")
logger.setLevel(logging.INFO)

class SpriteTriplet:
    def __init__(self):
        self.config = TripletConfig()

    async def invoke_ollama(self, port: int, model: str, prompt: str) -> str:
        """Simulates an API call to a fenced Ollama instance."""
        # Step 23.2: Intent-Verification Prefix [REQ]
        intent_prompt = f"[REQ] {prompt}"

        url = f"http://127.0.0.1:{port}/api/generate"
        payload = {"model": model, "prompt": intent_prompt, "stream": False}

        logger.info(f"Invoking {model} with intent prefix...")
        await asyncio.sleep(self.config.RATE_LIMIT_DELAY)

        # Step 23.2: Intent-Verification Prefix [ACK]
        return f"[ACK] [MOCK_RESPONSE from {model}]: Executed '{prompt[:20]}...'"

    async def l1_macro_process(self, global_instruction: str) -> str:
        """L1 (500M Master): Role: ARCHITECT. Operational Verb: DECOMPOSE."""
        # Step 23.1: Hyper-Specific Persona Sharding
        logger.info("--- L1 Master (ARCHITECT) Decomposing ---")
        prompt = f"DECOMPOSE into architectural steps: {global_instruction}"
        return await self.invoke_ollama(
            self.config.OLLAMA_PORTS["L1_MASTER"],
            self.config.MODELS["L1_MASTER"],
            prompt
        )

    async def l2_orchestrator_process(self, l1_output: str) -> str:
        """L2 (250M Orchestrator): Role: TRANSLATOR. Operational Verb: PROCEDURALIZE."""
        # Step 23.1: Hyper-Specific Persona Sharding
        logger.info("--- L2 Orchestrator (TRANSLATOR) Proceduralizing ---")
        prompt = f"PROCEDURALIZE into code steps: {l1_output}"
        prompt = prompt[:self.config.L2_CONTEXT_LIMIT]
        return await self.invoke_ollama(
            self.config.OLLAMA_PORTS["L2_ORCHESTRATOR"],
            self.config.MODELS["L2_ORCHESTRATOR"],
            prompt
        )

    async def l3_smoll_process(self, l2_output: str) -> str:
        """L3 (135m Smoll): Role: CODER. Operational Verb: SYNTAX_GENERATE."""
        # Step 23.1: Hyper-Specific Persona Sharding
        logger.info("--- L3 Smoll (CODER) Syntax Generating ---")
        prompt = f"SYNTAX_GENERATE final code: {l2_output}"
        prompt = prompt[:self.config.L3_CONTEXT_LIMIT]
        final_code = await self.invoke_ollama(
            self.config.OLLAMA_PORTS["L3_SMOLL"],
            self.config.MODELS["L3_SMOLL"],
            prompt
        )

        mock_code_payload = f"def execute_task():\n    # {final_code}\n    pass"
        return mock_code_payload

    async def run_cascade(self, global_instruction: str) -> dict:
        """Executes the full L1 -> L2 -> L3 cascade."""
        logger.info(f"Starting Industrial Cascade for: {global_instruction}")

        l1_out = await self.l1_macro_process(global_instruction)
        l2_out = await self.l2_orchestrator_process(l1_out)
        l3_out = await self.l3_smoll_process(l2_out)

        # Submit to Mock IDE
        async with httpx.AsyncClient() as client:
            try:
                ide_response = await client.post(
                    self.config.MOCK_IDE_URL,
                    json={
                        "agent_id": "Sprite-Triplet-Alpha",
                        "task_id": "task_cascade_001",
                        "code_payload": l3_out
                    }
                )
                ide_result = ide_response.json()
            except httpx.ConnectError:
                logger.error("Mock IDE is offline. Could not submit code.")
                ide_result = {"status": "offline", "message": "IDE Mock server not running on port 8001"}

        return {
            "l1_output": l1_out,
            "l2_output": l2_out,
            "l3_payload": l3_out,
            "ide_result": ide_result
        }
