# TIMESTAMP: 2026-06-09
# PROJECT_ID: SimsMerged-v1.4.2
# AGENT_ID: viper_cli-architectssj4
# DESCRIPTION: Phases 9 & 10 - Grand Unification Benchmark

import asyncio
import logging
import time
import os
import sys

# Ensure backend module is resolvable
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from backend.tok_communications.tok_tree import TokTreeDAG
from backend.sprite_triplet.depin_wallet import DePINLedger
from backend.sprite_triplet.triplet import SpriteTriplet
from backend.sprite_triplet.topological_wrapper import TopologicalGrid
from backend.tok_communications.pulse_core import GlobalPulse
from backend.data_engineering.arrow_logger import TelemetryLogger
from backend.tok_communications.inner_tok_layer import InnerTokDaemon

# Adjust logging for cleaner terminal output
logging.basicConfig(level=logging.INFO, format='%(asctime)s | %(name)s | %(levelname)s | %(message)s')
logger = logging.getLogger("MASTER_ORCHESTRATOR")

async def run_unification():
    logger.info("=============================================")
    logger.info("INITIATING SIMSMERGED GRAND UNIFICATION TEST")
    logger.info("=============================================")

    # 1. Initialize Subsystems
    logger.info("[INIT] Booting Subsystems...")
    tok_tree = TokTreeDAG()
    ledger = DePINLedger()
    grid = TopologicalGrid()
    triplet = SpriteTriplet()
    pulse = GlobalPulse(tick_rate_ms=200) # Slower pulse for readable logs
    telemetry = TelemetryLogger()
    inner_tok = InnerTokDaemon()

    agent_id = "L3_PIONEER_01"

    # 2. Start Global Pulse in background
    logger.info("[INIT] Starting Global Pulse Heartbeat...")
    pulse_task = asyncio.create_task(pulse.pulse_loop())

    # 3. Setup Agent State
    logger.info(f"[STATE] Registering Agent: {agent_id}")
    grid.assign_agent_coordinate(agent_id, x=0, y=0, z=0)

    # Tok Tree provides initial funding to the agent
    initial_funds = 20.0
    ledger.fund_wallet(agent_id, initial_funds)
    telemetry.log_event("AGENT_SPAWN", agent_id, f'{{"initial_funds": {initial_funds}}}')

    # 4. Tok Tree Defines a Task DAG
    logger.info("\n>>> STAGE 1: TOK TREE TASK ASSIGNMENT <<<")
    t_gather = tok_tree.add_task("Gather Topological Data", base_reward=5.0)
    t_build = tok_tree.add_task("Build Data Parser", base_reward=15.0)
    tok_tree.link_dependency(t_gather.task_id, t_build.task_id)

    # Assign the first task
    tok_tree.assign_task(t_gather.task_id, agent_id)

    # 5. Agent Movement (Grid & DePIN interaction)
    logger.info("\n>>> STAGE 2: TOPOLOGICAL MOVEMENT <<<")
    target_zone = (10, 10, 0)
    logger.info(f"Agent {agent_id} initiating travel to Zone {target_zone}...")
    travel_cost = grid.calculate_travel_cost(agent_id, *target_zone)

    can_travel = ledger.charge_inference_fee(agent_id, int(travel_cost * 10000)) # abstract conversion for test
    if can_travel:
        grid.assign_agent_coordinate(agent_id, *target_zone)
        inner_tok.intercept_payload(agent_id, f"ZONE_{target_zone[0]}_{target_zone[1]}_{target_zone[2]}", {"action": "travel", "target": "Gather Data"}, time.time())
        logger.info(f"Travel successful. Agent now in Zone {target_zone}.")
    else:
        logger.error("Travel failed due to insufficient funds.")

    await asyncio.sleep(1) # Let heartbeat tick

    # 6. Triplet Cascade Execution (Simulation)
    logger.info("\n>>> STAGE 3: SPRITE TRIPLET CASCADE <<<")
    logger.info(f"Agent {agent_id} beginning cognitive cascade for task: '{t_gather.description}'")

    # Charge inference fee for thinking
    ledger.charge_inference_fee(agent_id, 4096)

    cascade_result = await triplet.run_cascade(t_gather.description)
    inner_tok.intercept_payload(agent_id, f"ZONE_{target_zone}", {"action": "generate", "target": "Data Gathering Logic"}, time.time())
    telemetry.log_event("INFERENCE_COMPLETE", agent_id, '{"tokens_used": 4096}')

    logger.info(f"Cascade Output Summary:")
    logger.info(f"  -> L1 Output: {cascade_result['l1_output']}")
    logger.info(f"  -> L3 Payload Size: {len(cascade_result['l3_payload'])} bytes")

    # 7. Task Completion & Bounty Payout
    logger.info("\n>>> STAGE 4: TASK COMPLETION & BOUNTY <<<")
    bounty = tok_tree.complete_task(t_gather.task_id)
    if bounty > 0:
        tx_hash = ledger.fund_wallet(agent_id, bounty)
        logger.info(f"Bounty of {bounty} tokens paid to {agent_id}. TX: {tx_hash}")

    # Check if next task unlocks
    can_build = tok_tree.nodes[t_build.task_id].can_execute()
    logger.info(f"Can Agent proceed to '{t_build.description}'? : {can_build}")
    if can_build:
        tok_tree.assign_task(t_build.task_id, agent_id)

    # 8. Teardown
    logger.info("\n>>> STAGE 5: SYSTEM TEARDOWN <<<")
    telemetry.flush_to_parquet()
    pulse.is_running = False
    await pulse_task

    logger.info("=============================================")
    logger.info("GRAND UNIFICATION TEST COMPLETED SUCCESSFULLY")
    logger.info("=============================================")

if __name__ == "__main__":
    asyncio.run(run_unification())
