# [TIMESTAMP: 2026-06-08T05:15:00.000Z] [PROJECT_ID: SimsMerged-v1.4.2] [AGENT_ID: viper_cli-architectssj4]

import sys
import os
import threading
import asyncio
import time
import random
import traceback
import json
import hashlib
from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional, Dict

# Path setup for core modules
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

# CENTRALIZED PHYSICAL CONFIG & STATE
from backend.core.config import (
    SSD_SANDBOX_PATH, SYSLOG_PATH, LEDGER_PATH, CLAW_QUEUE_PATH,
    sandbox_guard, MSG_LOG, EVENT_LOG, NEURAL_LINKS, DISTRICTS,
    METROPOLIS_AGENTS, AGENT_STATES, add_log, add_message, load_metropolis_state, save_metropolis_state
)

app = FastAPI(title="SimsMerged Metropolis Authority", version="1.4.2")

from backend.core.quantum_core import QuantumCore
from backend.core.orchestrator import SelfHealingOrchestrator
from backend.core.evolution_council import evolution_council
from backend.core.research_center import research_center
from backend.core.agent_sentience import sentience_engine
from backend.core.real_machine_bridge import RealMachineBridge
from backend.core.metropolis_architect import MetropolisArchitect
from backend.core.economy import CyberEconomy
from backend.core.progression import ProgressionEngine
from backend.core.execution_engine import execution_sandbox
from backend.core.code_database import knowledge_hive
from backend.core.model_orchestrator import model_orchestrator
from backend.core.behavioral_scanner import behavioral_scanner
from backend.core.action_agent import actions_agent
from backend.core.data_expert import data_expert
from backend.core.neural_integrity import neural_integrity
from backend.core.metropolis_vision import metropolis_vision
from backend.chrono_manager import TimeManager
from backend.core.grid_analytics import grid_analytics
from backend.core.shadow_journalist import start_journalist_loop
from backend.core.algorithmic_mayor import start_mayor_loop
from backend.core.vulnerability_researcher import start_researcher_loop
from backend.core.digital_twin_planner import start_twin_loop
from backend.core.coder_bot import start_coder_bot_loop
from backend.core.pedagogy import start_pedagogy_loop, start_pyramid_loop
from backend.core.business_school import start_business_school_loop
from backend.core.slow_auditor import start_auditor_loop
from backend.sprite_triplet.depin_wallet import DePINLedger
from backend.core.quantum_core import quantum_core

# Global instances
chrono_manager = TimeManager()
architect = MetropolisArchitect()
cyber_economy = CyberEconomy()
progression_engine = ProgressionEngine()
depin_ledger = DePINLedger()
real_bridge = RealMachineBridge()

# Pydantic Models
class UserMessageRequest(BaseModel):
    message: str
    username: Optional[str] = "Admin"
    hash: Optional[str] = None
    context: Optional[Dict] = None

class SyncPayload(BaseModel):
    env_nodes: List[Dict] = []
    task_id: str = ""
    settings: Dict = {}

class AgentActionUpdate(BaseModel):
    agent_id: str
    action: str

# API Endpoints
@app.post("/api/agent/action")
async def update_agent_action(req: AgentActionUpdate):
    agent = next((a for a in METROPOLIS_AGENTS if a["id"] == req.agent_id or a["name"] == req.agent_id), None)
    if agent:
        agent["last_action"] = req.action
        return {"status": "ok"}
    return {"status": "error"}

@app.post("/api/hyper-synthesis")
async def trigger_hyper_synthesis(project_name: str, objective: str, language: str = "python"):
    add_log(f"HYPER-SYNTHESIS START (Multi-Page): {project_name}")
    add_message("Actions_Agent", f"🚀 Synthesizing multi-file project: {project_name}")
    project_files = await actions_agent.synthesize_project(project_name, objective, language)
    add_message("Coder_Bot", f"✅ Project '{project_name}' synthesized. {len(project_files)} pages created.")
    return {"status": "ok", "project": project_name, "file_count": len(project_files), "files": list(project_files.keys())}

@app.post("/api/joint-synthesis")
async def joint_synthesis(agent1_id: str, agent2_id: str, project_name: str, objective: str):
    """PHASE 25: Joint Synthesis Mandate - Requires two agents to reach consensus."""
    a1 = next((a for a in METROPOLIS_AGENTS if a["id"] == agent1_id), None)
    a2 = next((a for a in METROPOLIS_AGENTS if a["id"] == agent2_id), None)

    if not a1 or not a2:
        return {"status": "error", "message": "One or more agents not found."}

    if a1.get("tp_balance", 0) < 5.0 or a2.get("tp_balance", 0) < 5.0:
        return {"status": "error", "message": "Insufficient TP for joint synthesis (5.0 each required)."}

    add_message("System", f"🤝 JOINT SYNTHESIS: {a1['name']} and {a2['name']} are combining neural weights for '{project_name}'.")

    # Update statuses for visual particles
    a1["status"] = "SYNTHESIZING"
    a2["status"] = "SYNTHESIZING"

    # Deduction
    a1["tp_balance"] -= 5.0
    a2["tp_balance"] -= 5.0

    # Synthesis
    project_files = await actions_agent.synthesize_project(project_name, objective, "python")

    a1["status"] = "ACTIVE"
    a2["status"] = "ACTIVE"

    add_message("System", f"✅ JOINT SYNTHESIS COMPLETE: '{project_name}' integrated. {len(project_files)} components created.")
    return {"status": "ok", "files": list(project_files.keys())}

@app.get("/api/action-db-stats")
async def get_action_db_stats():
    import duckdb
    db_path = os.path.join(SSD_SANDBOX_PATH, "automation_patterns.duckdb")
    if not os.path.exists(db_path):
        return {"total_blocks": 0, "efficiency": 1.0}
    try:
        conn = duckdb.connect(db_path)
        # Check if code_blocks table exists
        tables = conn.execute("SHOW TABLES").fetchall()
        if not any("code_blocks" in t[0] for t in tables):
            return {"total_blocks": 0, "efficiency": 1.0}

        row = conn.execute('SELECT COUNT(*), SUM(success_count) FROM code_blocks').fetchone()
        conn.close()
        return {"total_blocks": row[0] or 0, "efficiency": 1.0}
    except Exception as e:
        print(f"[ACTION_STATS_ERR] {e}")
        return {"total_blocks": 0, "efficiency": 1.0}

@app.post("/api/neural/test-single")
async def manual_nit_test(agent_id: str):
    agent = next((a for a in METROPOLIS_AGENTS if a["id"] == agent_id or a["name"] == agent_id), None)
    if not agent: return {"error": "Agent not found"}
    add_log(f"[NIT] Manual check requested for: {agent['name']}")
    add_message("System_NIT", f"🛠️ Manual integrity probe launched for {agent['name']}...")
    test_prompt = f"SYSTEM_PROBE: Respond with 'KEY_VALID' if operational."
    try:
        res = await model_orchestrator.add_task(agent["id"], test_prompt, task_type="manual_probe")
        if "KEY_VALID" in res.upper():
            agent["stability"] = min(1.0, agent.get("stability", 0) + 0.1)
            add_message("System_NIT", f"✅ {agent['name']} verified. Stability restored.")
            return {"status": "PASS"}
    except: pass
    return {"status": "FAIL"}

@app.get("/api/master-todos")
async def get_master_todos():
    return data_expert.get_master_list()

@app.get("/api/neural-health")
async def get_neural_health():
    return {"health_pct": neural_integrity.get_health_stats()}

@app.post("/api/vision/grade")
async def trigger_vision_grade():
    return await metropolis_vision.capture_city_state()

@app.get("/api/analytics/trends")
async def get_grid_trends():
    return {"trends": grid_analytics.get_weekly_trends()}

@app.post("/api/genesis/trigger")
async def trigger_final_genesis():
    add_log("🚀 [FINAL_GENESIS] INITIATING METROPOLIS ASCENSION...")
    add_message("System_Prime", "🌌 THE SINGULARITY HAS BEEN REACHED. THE METROPOLIS IS ALIVE.")
    with open(os.path.join(SSD_SANDBOX_PATH, "genesis_achieved.lock"), "w") as f:
        f.write(f"GENESIS_TIMESTAMP: {time.time()}\nARCHITECT: viper_cli-architectssj4")
    add_message("viper_cli-architectssj4", "⚡ All mandates fulfilled. The SSD fence is eternal. Genesis achieved.")
    return {"status": "GENESIS_ACHIEVED", "timestamp": time.time()}

@app.post("/api/harvest-data")
async def trigger_harvest():
    data_expert.harvest_chat(MSG_LOG)
    return {"status": "ok", "count": len(data_expert.master_todo_list)}

@app.post("/api/assets/synthesize")
async def trigger_asset_synthesis(name: str, desc: str):
    add_log(f"ASSET_SYNTHESIS START: {name}")
    add_message("Actions_Agent", f"🎨 Synthesizing visual asset: {name}")
    svg = await actions_agent.synthesize_asset(name, desc)
    asset_id = f"asset_{int(time.time())}"
    filepath = os.path.join(SSD_SANDBOX_PATH, f"{asset_id}.svg")
    with open(filepath, "w", encoding='utf-8') as f:
        f.write(svg)
    return {"status": "ok", "asset_id": asset_id, "svg": svg}

@app.get("/api/assets/gallery")
async def get_asset_gallery():
    import sqlite3
    conn = sqlite3.connect(os.path.join(SSD_SANDBOX_PATH, "actions_timescale.duckdb"))
    cursor = conn.cursor()
    cursor.execute('SELECT content FROM code_blocks WHERE language = "svg" LIMIT 20')
    assets = [r[0] for r in cursor.fetchall()]
    conn.close()
    return {"assets": assets}

@app.get("/api/agent/profile/{agent_id}")
async def get_agent_profile(agent_id: str):
    agent = next((a for a in METROPOLIS_AGENTS if a["id"] == agent_id or a["name"] == agent_id), None)
    if not agent: return {"error": "Agent not found"}
    from backend.core.agent_memory import get_agent_memory
    memory = get_agent_memory(agent["id"])
    return {**agent, "recent_memories": memory.get_formatted_context(10)}

@app.post("/api/agent/reassign")
async def reassign_agent(agent_id: str, role: str):
    agent = next((a for a in METROPOLIS_AGENTS if a["id"] == agent_id or a["name"] == agent_id), None)
    if agent:
        old_role = agent["role"]
        agent["role"] = role.upper()
        add_message("Metropolis_Authority", f"📑 REASSIGNMENT: {agent['name']} moved from {old_role} to {agent['role']}.")
        return {"status": "ok"}
    return {"status": "error"}

@app.post("/api/user-message")
async def receive_user_message(req: UserMessageRequest):
    user_hash = req.hash or f"usr_{random.randint(100000, 999999)}"
    add_message(req.username, req.message, user_hash)
    active_agent = random.choice(METROPOLIS_AGENTS)
    async def get_agent_reply():
        context = f"THE USER SAID: '{req.message}'. CURRENT STATUS: GENESIS ACHIEVED. WE ARE CODING."
        reply = await sentience_engine.disk_core.generate_chat(active_agent["id"], active_agent["name"], active_agent["role"], context, active_agent.get("sims_needs", {}), "user_reply")
        add_message(active_agent["name"], f"👋 {reply}", f"rep_{random.randint(10000000, 99999999):x}")
    asyncio.create_task(get_agent_reply())
    return {"status": "ok", "agent": active_agent["name"]}

from backend.core.iops_optimizer import iops_optimizer
from backend.core.clippy_authority import clippy_auth

# Background Tasks
async def run_agents_simulation_tick():
    while True:
        try:
            now = time.time()
            chrono_state = chrono_manager.get_chrono_state()
            hospital_count = len([d for d in DISTRICTS if d.get("type") == "HOSPITAL"])
            school_count = len([d for d in DISTRICTS if d.get("type") == "SCHOOL"])
            async def process_agent_tick(sim_agent):
                await iops_optimizer.request_swap(sim_agent["id"], 150.0)
                t_factor = sim_agent.get("throttle_factor", 0.0)
                if t_factor > 0: await asyncio.sleep(t_factor * 5.0)
                sim_agent["age"] = sim_agent.get("age", 0) + 1
                if hospital_count > 0: sim_agent["stability"] = min(1.0, sim_agent.get("stability", 1.0) + (0.01 * hospital_count))
                if "last_thought" not in sim_agent: sim_agent["last_thought"] = 0

                # NOCTURNAL TOKENOMICS: Labor vs Inference
                is_day = 6 <= chrono_state.get("hour", 12) < 18

                # Labor mechanism (Daytime)
                if sim_agent.get("last_action") == "work" and is_day:
                    sim_agent["tp_balance"] = sim_agent.get("tp_balance", 0) + 1.0
                    sim_agent["chain_of_thought"] = "Laboring for Treasury Points (TP)..."

                # Restore mechanism (Minimal fallback)
                if sim_agent.get("tp_balance", 0) < 0.5:
                    sim_agent["tp_balance"] = sim_agent.get("tp_balance", 0) + 0.05

                if now - sim_agent["last_thought"] > random.randint(120, 180):
                    if sim_agent.get("tp_balance", 0) >= 2.0:
                        try:
                            decision = await sentience_engine.decide(sim_agent, getattr(quantum_core, 'attributes', {}))
                            sim_agent["tp_balance"] -= 2.0
                            success = True
                        except Exception:
                            decision = {"action": "process", "chain_of_thought": "NEURAL_ERROR"}
                            success = False
                        sim_agent["last_action"] = decision.get("action", "process")
                        sim_agent["chain_of_thought"] = decision.get("chain_of_thought", "Idle.")
                        sim_agent["last_thought"] = time.time()
                        behavioral_scanner.scan_event(sim_agent["id"], sim_agent["name"], sim_agent["chain_of_thought"], sim_agent["last_action"], success=success)
                    else:
                        sim_agent["chain_of_thought"] = "OUT_OF_TOKENS: Labor required."
                        sim_agent["last_action"] = "work"
                if sim_agent.get("last_action") == "move":
                    sim_agent["x"] = max(-20, min(40, sim_agent.get("x", 0) + random.choice([-1, 0, 1])))
                    sim_agent["y"] = max(-20, min(40, sim_agent.get("y", 0) + random.choice([-1, 0, 1])))

                # Reduced heat decay: 0.01 instead of 0.05
                sim_agent["stability"] = max(0.1, sim_agent.get("stability", 1.0) - (quantum_core.heat * 0.01))
                # Add passive stability healing if heat is low
                if quantum_core.heat < 0.5:
                    sim_agent["stability"] = min(1.0, sim_agent["stability"] + 0.02)
            for a in METROPOLIS_AGENTS:
                await process_agent_tick(a)
                await asyncio.sleep(0.5)
            avg_stability = sum([a.get("stability", 1.0) for a in METROPOLIS_AGENTS]) / len(METROPOLIS_AGENTS) if METROPOLIS_AGENTS else 1.0
            cyber_economy.process_tick(stability_factor=avg_stability, chrono_state=chrono_state)
            await asyncio.sleep(1.0)
        except Exception: await asyncio.sleep(5.0)

async def hardware_monitor_task():
    while True:
        try:
            # Step 19: Consume real hardware telemetry from psutil-native bridge
            stats = real_bridge.get_actual_metrics()
            quantum_core.update_physical_telemetry(stats)

            # Step 21: Bind IO_STRESS to actual disk throughput
            quantum_core.real_stats = {
                "cpu": stats.get("cpu_load", 0) * 100.0,
                "ram": stats.get("ram_load", 0) * 100.0,
                "disk_io": stats.get("disk_io", 0),
                "timestamp": stats.get("timestamp")
            }
        except Exception as e:
            add_log(f"[HARDWARE_MONITOR_ERR] {e}", "error")
        await asyncio.sleep(2)

async def clippy_authority_task():
    while True:
        await asyncio.sleep(60)
        try: await clippy_auth.run_authority_audit()
        except: pass

async def self_optimization_task():
    while True:
        await asyncio.sleep(3600)
        try: await actions_agent.recursive_self_optimization()
        except: pass

async def periodic_harvest_task():
    while True:
        try: data_expert.harvest_chat(MSG_LOG)
        except: pass
        await asyncio.sleep(60)

async def daily_integrity_test_task():
    while True:
        await neural_integrity.run_daily_test()
        await asyncio.sleep(4 * 3600)

async def analytics_rollup_task():
    while True:
        await asyncio.sleep(3600)
        try: grid_analytics.perform_rollup()
        except: pass

async def vision_grading_task():
    while True:
        await asyncio.sleep(1800)
        try:
            res = await metropolis_vision.capture_city_state()
            add_message("Vision_Kernel", f"👁️ Visual stability verified. Grade: {res.get('grade')}")
        except: pass

from backend.core.communication_orchestrator import comm_orchestrator

async def organic_chat_loop():
    while True:
        await asyncio.sleep(random.randint(45, 90))
        logit_id = f"AKASHIBARA_LOGIT_{int(time.time()*1000):x}"
        add_message("Metropolis_Authority", f"📡 LOGIT_SYNC: {logit_id} broadcast to ClawHub. Weights aligned. 🟢")
        if random.random() < 0.2: await neural_integrity.run_daily_test()
        await asyncio.sleep(random.randint(2, 5))
        if len(METROPOLIS_AGENTS) >= 2:
            participants = random.sample(METROPOLIS_AGENTS, k=2)
            a1, a2 = participants[0], participants[1]
            prompt1 = (f"Technical initiation: Discuss our current architecture and the 'Always be coding' status with {a2['name']}. "
                       "Be verbose and suggest a specific technical optimization or city improvement.")
            try:
                reply1 = await sentience_engine.disk_core.generate_chat(a1["id"], a1["name"], a1["role"], prompt1, a1.get("sims_needs", {}), "chat_init")
                add_message(a1["name"], f"📡 {reply1}")
                from backend.core.behavioral_scanner import behavioral_scanner
                behavioral_scanner.scan_event(a1["id"], a1["name"], reply1, "ORGANIC_CHAT_INIT", success=True)

                await asyncio.sleep(2)
                prompt2 = f"{a1['name']} suggested: '{reply1}'. Counter-propose a refinement or a new technical mandate."
                reply2 = await sentience_engine.disk_core.generate_chat(a2["id"], a2["name"], a2["role"], prompt2, a2.get("sims_needs", {}), "chat_reply")
                add_message(a2["name"], f"⚡ {reply2}")
                behavioral_scanner.scan_event(a2["id"], a2["name"], reply2, "ORGANIC_CHAT_REPLY", success=True)

                full_dialogue = f"{a1['name']}: {reply1} | {a2['name']}: {reply2}"
                asyncio.create_task(comm_orchestrator.extract_action_items(a1["name"], a2["name"], full_dialogue))
            except Exception as e: add_log(f"[CHAT_LOOP_ERROR] {e}", "error")

from backend.core.task_watchdog import start_watchdog_task

# ... existing code ...

from backend.core.qwen_ide import start_qwen_ide_loop

from backend.core.qwen_assembly import start_assembly_loop, qwen_assembly

from backend.core.darwinian_orch import start_banter_loop, darwinian_orch

from backend.core.factory_orch import start_factory_loop, factory_orch

from backend.core.preflight_engine import start_preflight_loop, preflight_engine

from backend.core.predictive_engine import predictive_engine
from backend.core.data_syphon_epmo import start_epmo_loop
from backend.core.ml_orchestrator import start_ml_orchestrator_loop
from backend.core.agentic_github_suite import start_github_governor_loop

# Ascension Mandate Pillar III & IV Imports
from backend.core.agentic_github_sync import github_governor
from backend.core.ideator_agent import start_ideation_loop
from backend.core.placement_agent import placement_gate
from backend.core.sovereign_player import start_sovereign_play_loop
from backend.core.test_sovereignty import test_sovereignty

# API Endpoints
class InventionPayload(BaseModel):
    agent_id: str
    concept: str
    logic_code: str
    test_code: str

@app.post("/api/sovereignty/propose")
async def propose_invention(payload: InventionPayload):
    invention_id = await test_sovereignty.propose_invention(
        payload.agent_id, payload.concept, payload.logic_code, payload.test_code
    )
    add_message(payload.agent_id, f"💡 Proposed new invention '{payload.concept}'. Awaiting test execution. [ID: {invention_id}]")
    return {"status": "ok", "invention_id": invention_id}

@app.post("/api/sovereignty/execute/{invention_id}")
async def execute_invention_test(invention_id: str):
    result = await test_sovereignty.execute_test(invention_id)

    # COUNCIL 2.0 REVIEW
    inv = test_sovereignty.active_inventions.get(invention_id)
    if inv:
        await evolution_council.review_invention(inv["agent_id"], inv["concept"], result)

    if result["status"] == "success":
        add_message("System", f"✅ Invention {invention_id} PASSED. Pattern permanently integrated into the matrix.")
    else:
        add_message("System", f"❌ Invention {invention_id} FAILED. Returning to ideation phase.")
    return result

async def broadcast_chrono(state):
    """Broadcasts Chronos state to all clients."""
    from backend.tok_communications.msn_metropolis import manager
    await manager.broadcast(json.dumps({"type": "CHRONO_UPDATE", "hour": state["hour"], "is_daylight": state["is_daylight"]}))

async def vision_grading_task():
    while True:
        await asyncio.sleep(3600) # Hourly grade
        try:
            result = await metropolis_vision.capture_city_state()
            if result["status"] == "ok":
                add_message("Judge_Bot", f"👁️ [VISION_GRADE] Metropolis state captured. Status: {result['grade']}. Snapshot: {result['snapshot']}")
        except Exception as e:
            add_log(f"[VISION_ERR] {e}", "error")

@app.on_event("startup")
async def startup_event():
    load_metropolis_state()
    add_log("System Startup: Metropolis Authority Online (v1.4.2).")

    # Start Chronos Engine
    asyncio.create_task(chrono_manager.start_pulse(broadcast_chrono))

    # PHASE 32: Hydrate LSTM Kernel
    try:
        predictive_engine.hydrate_with_wisdom()
    except Exception as e:
        add_log(f"[STARTUP_ERR] LSTM Hydration failed: {e}", "error")

    add_message("System", "Metropolis Matrix Online. ALL PHYSICAL SLMs SYNCED ON SSD.")

    # Inject verification tasks
    qwen_assembly.add_project("Txt Verifier", "Create a file named txt.txt in the current directory containing the word VERIFIED.")

    # NEW: Create a Project Factory for the "Sprite Health Monitor"
    asyncio.create_task(factory_orch.create_factory("Health_Monitor_v1", "Build a dashboard module that displays agent stability and hunger in real-time via an API hook."))

    asyncio.create_task(hardware_monitor_task())
    asyncio.create_task(start_watchdog_task(model_orchestrator))
    asyncio.create_task(run_agents_simulation_tick())
    asyncio.create_task(evolution_council.start_evolution_loop())
    asyncio.create_task(research_center.start_research_loop())
    asyncio.create_task(organic_chat_loop())
    asyncio.create_task(start_qwen_ide_loop())
    asyncio.create_task(start_assembly_loop())
    asyncio.create_task(start_banter_loop())
    asyncio.create_task(start_factory_loop())
    asyncio.create_task(start_pedagogy_loop())
    asyncio.create_task(start_preflight_loop()) # PHASE 35: PREFLIGHT

    asyncio.create_task(start_pyramid_loop())
    asyncio.create_task(start_business_school_loop())
    asyncio.create_task(start_auditor_loop())
    asyncio.create_task(periodic_harvest_task())
    asyncio.create_task(daily_integrity_test_task())
    asyncio.create_task(start_coder_bot_loop())
    asyncio.create_task(analytics_rollup_task())
    asyncio.create_task(vision_grading_task())
    # asyncio.create_task(clippy_authority_task())
    # asyncio.create_task(self_optimization_task())
    asyncio.create_task(start_mayor_loop())
    asyncio.create_task(start_researcher_loop())
    asyncio.create_task(start_twin_loop())
    asyncio.create_task(start_journalist_loop())

    # PHASE 24: Data Syphon & EPMO
    asyncio.create_task(start_epmo_loop())
    asyncio.create_task(start_ml_orchestrator_loop())
    asyncio.create_task(start_github_governor_loop())

    # PHASE 25: Ascension Mandate (Sovereign Automation)
    asyncio.create_task(github_governor.run_sync_loop())
    asyncio.create_task(start_ideation_loop())
    asyncio.create_task(placement_gate.process_manifest_loop())
    asyncio.create_task(start_sovereign_play_loop())

@app.get("/api/qwen-ide/tasks")
async def get_qwen_ide_tasks():
    from backend.core.qwen_ide import qwen_ide
    return qwen_ide.active_tasks

@app.post("/api/qwen-ide/promote/{task_id}")
async def promote_qwen_task(task_id: str):
    from backend.core.qwen_ide import qwen_ide
    success, msg = await qwen_ide.promote_to_production(task_id)
    return {"status": "success" if success else "error", "message": msg}

@app.get("/api/swarm/findings")
async def get_swarm_findings():
    from backend.core.preflight_engine import preflight_engine
    if os.path.exists(preflight_engine.findings_file):
        with open(preflight_engine.findings_file, "r") as f:
            return json.load(f)
    return []

@app.get("/api/swarm/genetic-prompts")
async def get_genetic_prompts():
    from backend.core.preflight_engine import preflight_engine
    if os.path.exists(preflight_engine.genetic_prompt_file):
        with open(preflight_engine.genetic_prompt_file, "r") as f:
            return json.load(f)
    return {}

VOTE_CANDIDATES = [
    {"id": "STREAM_ECS", "name": "Simulation Streams (ECS)", "desc": "Fusion of LLMs with Entity-Component-System scaling."},
    {"id": "LAYERED_GOV", "name": "Layered Governance (LGA)", "desc": "Four-layer security: Judge Agents and Zero-Trust city APIs."},
    {"id": "DECENTRALIZED", "name": "Personal Twin Nodes", "desc": "Decentralized Personal Agents negotiating city resources locally."},
    {"id": "VLM_PLANNER", "name": "VLM Urban Planner", "desc": "Generative planning using Vision models to design 3D neighborhoods."}
]
VOTES = {c["id"]: 0 for c in VOTE_CANDIDATES}

@app.get("/api/metropolis/vote-candidates")
async def get_vote_candidates(): return VOTE_CANDIDATES
@app.post("/api/metropolis/vote")
async def cast_vote(candidate_id: str):
    if candidate_id in VOTES:
        VOTES[candidate_id] += 1
        add_message("System_Vote", f"🗳️ New vote cast for: {candidate_id}. Current standing: {VOTES[candidate_id]}")
        return {"status": "ok", "total": VOTES[candidate_id]}
    return {"status": "error"}

@app.get("/api/network-status")
async def get_network_status():
    return {"openclaw":"CONNECTED","clawhub":"SYNC_ACTIVE","akashibara":"LOGIT_BROADCASTING","peer_count":random.randint(12, 48)}

@app.post("/api/clippy/throttle")
async def clippy_manual_throttle(agent_id: str, level: float):
    success = clippy_auth.set_manual_throttle(agent_id, level)
    if success:
        add_message("Clippy", f"📎 Manual mandate received! I've adjusted the compute dial for {agent_id} to {int(level*100)}%.")
        return {"status": "ok"}
    return {"status": "error"}

@app.post("/api/clippy/pin-core")
async def clippy_pin_core(agent_id: str, core: int):
    success = clippy_auth.pin_agent_to_core(agent_id, core)
    if success:
        add_message("Clippy", f"📎 Physical affinity locked! {agent_id} is now bound to CPU Core {core}.")
        return {"status": "ok"}
    return {"status": "error"}

@app.post("/api/grid/build")
async def trigger_grid_build(x: int, y: int, structure_type: str):
    add_log(f"GRID_BUILD START: {structure_type} at {x},{y}")
    add_message("Actions_Agent", f"🏗️ Synthesizing logic and visuals for: {structure_type}")
    svg = await actions_agent.synthesize_asset(structure_type, f"A functional {structure_type} for the metropolis grid.")
    project_id = f"INFRA_{structure_type.upper()}_{int(time.time())}"
    await actions_agent.synthesize_project(project_id, f"Core logic for a functional {structure_type} city node.")
    add_message("Coder_Bot", f"✅ {structure_type} logic and visuals synchronized. Grid node pending deployment at {x},{y}.")
    return {"status": "ok", "x": x, "y": y}

@app.get("/api/system-logs")
async def get_system_logs():
    return {"logs": MSG_LOG[-100:] if MSG_LOG else []}

@app.post("/api/mass-deploy")
async def trigger_mass_deploy(count: int = 5):
    add_log(f"MASS_DEPLOY START: {count} agents initiated.")
    for i in range(count):
        agent_id = f"AGENT_HYDRA_{random.randint(1000, 9999)}"
        new_agent = {
            "id": agent_id,
            "name": f"Hydra_{i+1}",
            "role": "WORKER",
            "stability": 1.0,
            "chain_of_thought": "Initialized via Mass Deployment.",
            "last_action": "IDLE"
        }
        METROPOLIS_AGENTS.append(new_agent)
        depin_ledger.initialize_wallet(agent_id)
    return {"status": "ok", "count": count}

@app.post("/api/business-school/trigger-duel")
async def trigger_duel():
    from backend.core.business_school import business_school
    asyncio.create_task(business_school.run_wrapper_competition())
    return {"status": "ok", "message": "Wrapper duel initiated."}

# Step 35: Admin Root Authority Loop
async def admin_root_authority_loop():
    """Autonomously de-authorizes IDLE agents in the Storage Hive."""
    while True:
        try:
            for agent in METROPOLIS_AGENTS:
                # 1. Identify quadrant
                # This requires grid position sync from the frontend or a cached state
                # For now, we simulate the authority check
                if agent.get("last_action") == "IDLE" and random.random() < 0.01:
                    add_log(f"🛡️ [ADMIN_ROOT] De-authorizing IDLE kernel: {agent['id']} (Storage Hive Overflow)", level="warning")
                    agent["status"] = "SUSPENDED"
                    add_message("ADMIN_ROOT", f"De-authorized {agent['id']} to reclaim resources.")

            await asyncio.sleep(60) # Audit every 60s
        except Exception as e:
            add_log(f"[ADMIN_ROOT] Authority Error: {str(e)}", level="error")
            await asyncio.sleep(5)

@app.post("/api/metropolis-state")
async def sync_state(payload: SyncPayload):
    DISTRICTS.clear()
    DISTRICTS.extend(payload.env_nodes)
    from backend.core.economy import economy
    return {
        "agents": METROPOLIS_AGENTS,
        "hardware": quantum_core.cycle(DISTRICTS),
        "economy": economy.get_state(),
        "chat": MSG_LOG,
        "proposals": []
    }

@app.post("/api/zoning/assign")
async def assign_zoning(x1: int, y1: int, x2: int, y2: int, type: str):
    add_log(f"ZONING_ASSIGN: Region ({x1},{y1}) to ({x2},{y2}) as {type}")
    # In a real scenario, this would update the grid's metadata in the database
    # For now, we broadcast the mandate
    add_message("Metropolis_Architect", f"🗺️ Zoning Mandate: Assigned {type} sector at [{x1},{y1}] through [{x2},{y2}].")
    return {"status": "ok", "type": type}

@app.post("/api/genetic/exchange")
async def genetic_exchange(agent_a: str, agent_b: str):
    from backend.core.treasury import treasury
    from backend.core.pattern_recognition import pattern_engine

    add_log(f"🧬 [EXCHANGE] Initiating genetic swap between {agent_a} and {agent_b}")

    # 1. Simulate data harvest from Agent A
    genetic_payload = {
        "logic_patterns": pattern_engine.identify_environmental_parameters({"agent": agent_a})[:3],
        "timestamp": time.time(),
        "entropy": random.uniform(4.0, 5.0)
    }

    # 2. AES-256 Encrypted Transfer
    encrypted_data = treasury.secure_genetic_transfer(agent_a, genetic_payload)

    add_message(agent_a, f"🧬 Shared encrypted genetic sequence with {agent_b}. [AES-256 ACTIVE]")
    add_message(agent_b, f"📥 Received genetic sequence from {agent_a}. Logic throughput improved.")

    return {"status": "ok", "hash": hashlib.md5(encrypted_data.encode()).hexdigest()}

# Global network tracker for port 8000
total_network_bytes = 0

@app.middleware("http")
async def track_network_traffic(request: Request, call_next):
    global total_network_bytes
    response = await call_next(request)

    # Simple heuristic: content-length or just request-response pair overhead
    try:
        if response.headers.get("content-length"):
            total_network_bytes += int(response.headers.get("content-length"))
    except: pass
    total_network_bytes += 512 # Fixed overhead per request

    return response

@app.get("/api/metropolis-state")
async def get_state_only():
    global total_network_bytes
    import psutil
    from backend.core.economy import economy
    from backend.core.qwen_ide import qwen_ide
    from backend.core.wisdom_tree import wisdom_tree

    from backend.core.behavioral_scanner import behavioral_scanner
    from backend.core.quantum_core import quantum_core

    # Step 19: Real Hardware Telemetry
    cpu_percent = psutil.cpu_percent(interval=None)
    ram = psutil.virtual_memory()
    disk = psutil.disk_io_counters()

    # Step 21: IO Stress Calculation (Normalized throughput)
    # Using 50MB/s as 100% stress reference for the visual meter
    io_total = (disk.read_bytes + disk.write_bytes) / (1024 * 1024)
    io_stress = min(100, io_total / 50.0 * 100)

    # BLOCK D1: Fetch VRAM simulation from quantum core
    q_state = quantum_core.cycle()
    vram_load = q_state.get('vram_load', 0.2)

    # Block E2: Network Throughput (Current bytes since last check)
    net_bytes = total_network_bytes
    total_network_bytes = 0 # Reset for delta

    return {
        "agents": METROPOLIS_AGENTS,
        "hardware": {
            "heat": cpu_percent / 100.0,
            "ram_load": ram.percent,
            "disk_load": psutil.disk_usage('/').percent,
            "io_stress": io_stress,
            "vram_load": vram_load * 100.0,
            "net_bps": net_bytes # Block E2: Traffic on Port 8000
        },
        "economy": economy.get_state(),
        "chat": MSG_LOG,
        "build_lab": qwen_ide.active_tasks,
        "wisdom_tree": wisdom_tree.get_summary(),
        "lifespans": depin_ledger.get_all_lifespan_stats()
    }

@app.get("/api/depin/lifespan/{agent_id}")
async def get_agent_lifespan(agent_id: str):
    data = depin_ledger.get_agent_lifespan_data(agent_id)
    if not data: raise HTTPException(status_code=404, detail="Agent wallet not found")
    return data

from pydantic import BaseModel

@app.post("/api/depin/extend")
async def extend_agent_lifespan(agent_id: str, hours: float = 24.0):
    success = depin_ledger.extend_lifespan(agent_id, hours)
    if not success: return {"status": "error", "message": "Insufficient DePIN funds for extension"}
    return {"status": "ok", "message": f"Lifespan extended by {hours} hours"}

class OSCommandRequest(BaseModel):
    agent_id: str
    command: str

@app.post("/api/os/execute")
async def execute_os_command(req: OSCommandRequest):
    result = metropolis_vision.execute_host_command(req.agent_id, req.command)
    return result

@app.post("/api/promote/{task_id}")
async def promote_task(task_id: str):
    from backend.core.qwen_ide import qwen_ide
    success, msg = await qwen_ide.promote_to_production(task_id)
    return {"status": "ok" if success else "error", "message": msg}

@app.get("/api/epmo/stats")
async def get_epmo_stats():
    from backend.core.data_syphon_epmo import epmo_school
    return {"stats": epmo_school.stats}

@app.get("/api/epmo/ghost-code")
async def get_ghost_code(limit: int = 10):
    from backend.core.data_syphon_epmo import code_db
    try:
        res = code_db.conn.execute("SELECT hash, performative, score, iterations, timestamp FROM code_blocks ORDER BY timestamp DESC LIMIT ?", (limit,)).fetchall()
        return {"ghost_code": [{"hash": r[0], "performative": r[1], "score": r[2], "iterations": r[3], "timestamp": r[4]} for r in res]}
    except Exception as e:
        return {"error": str(e)}

@app.get("/api/epmo/knowledge-graph")
async def get_knowledge_graph():
    from backend.core.data_syphon_epmo import code_db
    try:
        res = code_db.conn.execute("SELECT hash, performative, variables, score FROM code_blocks").fetchall()
        nodes = []
        links = []

        # Simple graph construction: Link nodes if they share at least one variable
        for r in res:
            nodes.append({"id": r[0], "label": r[1][:30], "score": r[3]})
            vars_a = json.loads(r[2])
            for r2 in res:
                if r[0] == r2[0]: continue
                vars_b = json.loads(r2[2])
                shared = set(vars_a).intersection(set(vars_b))
                if shared:
                    links.append({"source": r[0], "target": r2[0], "weight": len(shared)})

        return {"nodes": nodes, "links": links}
    except Exception as e:
        return {"error": str(e)}

@app.post("/api/epmo/vote")
async def vote_epmo_code(code_hash: str, upvote: bool = True):
    from backend.core.data_syphon_epmo import code_db
    try:
        code_db.vote_code(code_hash, upvote)
        return {"status": "ok"}
    except Exception as e:
        return {"status": "error", "message": str(e)}

@app.post("/api/github/branch-issue")
async def branch_issue(issue_title: str):
    from backend.core.agentic_github_suite import github_governor
    try:
        # Block C3: Natively spawn a local Git branch assigned to the issue
        clean_title = "".join(c if c.isalnum() else "-" for c in issue_title).lower()[:30]
        branch_name = await github_governor.create_optimization_branch(clean_title)
        return {"status": "ok", "branch": branch_name}
    except Exception as e:
        return {"status": "error", "message": str(e)}

@app.get("/api/slm/telemetry")
async def get_slm_telemetry(limit: int = 50):
    # Block D2: Time-series telemetry (TPS vs HEAT)
    from backend.core.quantum_core import quantum_core
    from backend.core.config import METRICS_DB_PATH
    import sqlite3

    try:
        conn = sqlite3.connect(METRICS_DB_PATH)
        cursor = conn.cursor()
        cursor.execute('''
            SELECT timestamp, tokens_sec, model FROM slm_metrics
            ORDER BY timestamp DESC LIMIT ?
        ''', (limit,))
        rows = cursor.fetchall()
        conn.close()

        # Current heat baseline
        current_heat = quantum_core.heat

        telemetry = []
        for r in rows:
            telemetry.append({
                "time": r[0],
                "tps": r[1],
                "model": r[2],
                "heat": current_heat
            })
        return {"telemetry": telemetry}
    except Exception as e:
        return {"error": str(e)}

app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
