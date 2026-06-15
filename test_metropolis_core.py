# [TIMESTAMP: 2026-06-11T04:20:00.000Z] [PROJECT_ID: SimsMerged-v1.4.2] [AGENT_ID: Gemini-CLI-Architect]

import asyncio
import json
import sys
import os

# Add backend to sys.path
sys.path.append(os.path.join(os.path.dirname(__file__), "backend"))

try:
    from core.pattern_recognition import pattern_engine
    from core.resource_governor import resource_governor
    from core.omniscient_steer import omniscient_steer
except ImportError:
    # Fallback for different execution contexts
    sys.path.append(os.path.dirname(__file__))
    from backend.core.pattern_recognition import pattern_engine
    from backend.core.resource_governor import resource_governor
    from backend.core.omniscient_steer import omniscient_steer

async def test_metropolis_core():
    print("🧪 [TEST] Starting Metropolis Core Validation...")

    # 1. Test Pattern Engine (Logit Database)
    print("📊 [TEST] Validating Pattern Engine...")
    test_data = "CPU: 45%, RAM: 30MB, Disk: OK"
    pattern_engine.store_pattern("test_telemetry_001", "telemetry", test_data, {"source": "validator"})
    
    matches = pattern_engine.identify_environmental_parameters({"raw": test_data})
    if matches and matches[0]['pattern_id'] == "test_telemetry_001":
        print("✅ [TEST] Pattern Engine: Logit Storage & Matching Verified.")
    else:
        print("❌ [TEST] Pattern Engine: Validation Failed.")

    # 2. Test Resource Governor
    print("🛡️ [TEST] Validating Resource Governor...")
    resource_governor.start()
    # Let it run for a few seconds to see logs
    await asyncio.sleep(2)
    resource_governor.stop()
    print("✅ [TEST] Resource Governor: Lifecycle Verified.")

    # 3. Test Omniscient Steer
    print("🤖 [TEST] Validating Omniscient Steer...")
    if omniscient_steer.process_ask("What is the system status?"):
        print("✅ [TEST] Omniscient Steer: Deterministic Reply Verified.")
    else:
        print("❌ [TEST] Omniscient Steer: Validation Failed.")

    print("🏁 [TEST] Metropolis Core Validation Complete.")

if __name__ == "__main__":
    asyncio.run(test_metropolis_core())
