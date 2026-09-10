# TIMESTAMP: 2026-06-09
# PROJECT_ID: SimsMerged-v1.4.2
# AGENT_ID: viper_cli-architectssj4
# DESCRIPTION: Logit Distribution Simulator (Drives the LogitChartPlugin)

import json
import time
import httpx
import asyncio
import random
import math

async def simulate_logits():
    print("[SIM] Starting Logit Telemetry Stream...")

    async with httpx.AsyncClient() as client:
        while True:
            # Generate a "Raw Reasoning Strength" distribution (Bell Curve style)
            size = 50
            mean = random.uniform(10, 40)
            std_dev = random.uniform(2, 10)

            logits = []
            for i in range(size):
                # Normal distribution formula approximation
                val = math.exp(-0.5 * ((i - mean) / std_dev) ** 2) * random.uniform(0.8, 1.2) * 50
                logits.append(round(val, 2))

            payload = {
                "type": "LOGIT_UPDATE",
                "data": logits
            }

            try:
                await client.post("http://127.0.0.1:8000/api/v1/agent/update", json=payload)
            except Exception as e:
                print(f"[SIM] Broadcast failed: {e}")

            await asyncio.sleep(0.5) # 2 Hz update rate

if __name__ == "__main__":
    try:
        asyncio.run(simulate_logits())
    except KeyboardInterrupt:
        print("\n[SIM] Stream halted.")
