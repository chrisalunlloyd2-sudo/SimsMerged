# TIMESTAMP: 2026-06-09
# PROJECT_ID: SimsMerged-v1.4.2
# AGENT_ID: viper_cli-architectssj4
# DESCRIPTION: Section B, Phase 4 - Chat Extractor Module

import time
import logging
import httpx
import asyncio

logger = logging.getLogger("ChatExtractor")
logger.setLevel(logging.INFO)

class ChatExtractor:
    def __init__(self, chat_api_url: str = "http://127.0.0.1:8002/api/v1/chat/send"):
        self.chat_api_url = chat_api_url

    async def extract_coordinate_change(self, agent_id: str, old_coord: tuple, new_coord: tuple):
        """Step 31 & 33: Correlate coordinate changes to automated chat updates."""
        if old_coord != new_coord:
            msg = f"moved from Zone {old_coord} to Zone {new_coord}."
            await self._push_to_chat(agent_id, "System", msg)

    async def extract_compiler_error(self, agent_id: str, error_msg: str):
        """Step 35: Translate compiler errors into chat apologies."""
        # Simulated LLM tone adjustment
        apology = f"Oops, I hit a snag while compiling: '{error_msg}'. Attempting a fix now. 🛠️"
        await self._push_to_chat(agent_id, "Development", apology)

    async def extract_depin_update(self, agent_id: str, amount: float, reason: str):
        """Step 37: Add visual tags for DePIN balance updates."""
        if amount > 0:
            msg = f"🤑 Received {amount} tokens for: {reason}"
        else:
            msg = f"💸 Burned {abs(amount)} tokens for: {reason}"
        await self._push_to_chat(agent_id, "Economy", msg)

    async def _push_to_chat(self, sender: str, channel: str, content: str):
        payload = {
            "sender_id": sender,
            "channel": channel,
            "message": content,
            "is_agent": True
        }
        async with httpx.AsyncClient() as client:
            try:
                response = await client.post(self.chat_api_url, json=payload)
                if response.status_code == 200:
                    logger.info(f"Extractor pushed msg from {sender} to #{channel}")
                else:
                    logger.warning(f"Failed to push message: {response.text}")
            except httpx.ConnectError:
                logger.error("MSN Metropolis Chat API is offline. Cannot extract message.")

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)

    async def run_extractor_test():
        extractor = ChatExtractor()

        # Note: This will log an error in the test because MSN Metropolis (uvicorn) isn't running in the background yet.
        # This is expected behavior for this isolated unit test.
        logger.info("Simulating Agent Movement...")
        await extractor.extract_coordinate_change("L3_MINER", (0,0,0), (1,0,0))

        logger.info("Simulating DePIN Transaction...")
        await extractor.extract_depin_update("L3_BUILDER", 15.0, "Completing Cabin Blueprint")

        logger.info("Simulating Compiler Failure...")
        await extractor.extract_compiler_error("L3_SMOLL", "SyntaxError: invalid syntax (line 4)")

    asyncio.run(run_extractor_test())
