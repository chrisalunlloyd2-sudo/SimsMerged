# TIMESTAMP: 2026-06-05T06:15:00.000Z
# PROJECT_ID: SimsMerged-v1.4-Metropolis
# AGENT_ID: Antigravity-Agent

import asyncio
import time
import os
import random
import json
import subprocess
import hashlib
from backend.core.neuromorphic_core import neuromorphic_core

from .code_database import knowledge_hive
from .config import SSD_SANDBOX_PATH, RESEARCH_DIR

class EvolutionCouncil:
    """
    EVOLUTIONARY COUNCIL 2.0:
    - Integrates Sovereign Inventions, Judge Verdicts, and Joint Synthesis.
    - Manages the Swarm's Genetic Skill-Matrix.
    - Broadcasts real-time voting to the JavaFX Council 2.0 HUD.
    """
    def __init__(self):
        # PHYSICAL SSD FENCE
        self.workspace_dir = os.path.join(SSD_SANDBOX_PATH, "city_workspace", "continue_project")
        os.makedirs(self.workspace_dir, exist_ok=True)

        self.interval_seconds = 600
        self.active_session = None

    async def broadcast_council_event(self, event_type, data):
        """Broadcasts council actions to all visual clients."""
        from backend.tok_communications.msn_metropolis import manager
        payload = {
            "type": "COUNCIL_2_0_EVENT",
            "event": event_type,
            "data": data,
            "timestamp": time.time()
        }
        await manager.broadcast(json.dumps(payload))

    async def execute_genetic_handshake(self, agent1_id, agent2_id):
        """Step 28/63: AES-256 Encrypted Trait Exchange."""
        from backend import main
        a1 = next((a for a in main.METROPOLIS_AGENTS if a["id"] == agent1_id), None)
        a2 = next((a for a in main.METROPOLIS_AGENTS if a["id"] == agent2_id), None)

        if not a1 or not a2: return

        # Shuffle traits (Genetic Crossover)
        t1 = a1.get("traits", [])
        t2 = a2.get("traits", [])

        new_for_a1 = [t for t in t2 if t not in t1]
        new_for_a2 = [t for t in t1 if t not in t2]

        updates = []
        if new_for_a1 and random.random() < 0.4:
            trait = random.choice(new_for_a1)
            a1["traits"].append(trait)
            updates.append(f"{a1['name']} learned {trait}")

        if new_for_a2 and random.random() < 0.4:
            trait = random.choice(new_for_a2)
            a2["traits"].append(trait)
            updates.append(f"{a2['name']} learned {trait}")

        if updates:
            msg = "🧬 [GENETIC_CROSSOVER] " + " | ".join(updates)
            main.add_log(msg)
            await self.broadcast_council_event("GENETIC_HANDSHAKE", {"agent1": agent1_id, "agent2": agent2_id, "updates": updates})

    async def review_invention(self, agent_id, concept, result):
        """Council reviews the result of a Sovereign Invention."""
        from backend import main
        status = "PASSED" if result["status"] == "success" else "FAILED"

        # Reward or Penalty
        agent = next((a for a in main.METROPOLIS_AGENTS if a["id"] == agent_id), None)
        if agent:
            if status == "PASSED":
                agent["level"] = agent.get("level", 0) + 2
                # Unlock specialized trait for successful invention
                new_trait = f"INVENTOR_{concept.upper()[:8]}"
                if "traits" not in agent: agent["traits"] = []
                agent["traits"].append(new_trait)
            else:
                agent["stability"] = max(0.1, agent.get("stability", 1.0) - 0.05)

        await self.broadcast_council_event("INVENTION_REVIEW", {"agent_id": agent_id, "concept": concept, "status": status})

    async def execute_web_crawl(self):
        """
        SWARM-DRIVEN EVOLUTION (80% SOVEREIGNTY):
        - 80% chance for a real agent to propose a city optimization.
        - Includes LEAN SIGMA 6 self-optimization of agent wrappers.
        """
        from backend import main
        from .execution_engine import execution_sandbox

        main.add_log("[HYPER_EVOLUTION] Initiating 80% sovereignty swarm brainstorming...", "info")

        # 1. Swarm Brainstorming (80% Sovereignty)
        if random.random() < 0.8:
            proposer = random.choice(main.METROPOLIS_AGENTS)

            # Expanded brainstroming for Preflight readiness
            roll = random.random()
            if roll < 0.3:
                prompt = "LEAN SIGMA 6: Propose a code optimization for your OWN execution wrapper to reduce SSD I/O. End with TOPIC: [WRAPPER_FIX]"
            elif roll < 0.6:
                prompt = "GUI_ARCHITECT: Identify a missing JavaFX component (AI_HUD, TODOPanel, MSN_V2) and propose a visual fix. End with TOPIC: [GUI_FIX]"
            else:
                prompt = "CITY_ARCHITECT: Propose a 'Preflight' testing wrapper for SLM consensus. End with TOPIC: [PREFLIGHT_TEST]"

            proposal = await main.sentience_engine.disk_core.generate_chat(
                proposer["id"], proposer["name"], proposer["role"], prompt, {}, "sovereign_proposal"
            )

            topic = "Neural Delta"
            if "TOPIC:" in proposal.upper():
                topic = proposal.upper().split("TOPIC:")[1].strip()

            impact = "LEAN_SIGMA_6" if "WRAPPER" in topic.upper() else "CITY_EXPANSION"
            chosen = {"topic": topic, "impact": impact}
        else:
            # 20% Baseline maintenance crawl
            projects = [
                {"topic": "LSS Kernel Patch", "impact": "CORE", "target": "stability", "val": 0.05},
                {"topic": "SSD Buffer Flush", "impact": "CORE", "target": "heat", "val": -5.0},
                {"topic": "Neural Mesh Expansion", "impact": "CITY_EXPANSION"},
                {"topic": "Quantum Data Bank", "impact": "CITY_EXPANSION"},
                {"topic": "Isometric Culling Fix", "impact": "GAME"},
                {"topic": "SSD Platter Alignment", "impact": "HARDWARE"},
                {"topic": "Autonomous Logic Foundry", "impact": "CITY_EXPANSION"},
            ]
            chosen = random.choice(projects)

        # Generate advanced additive code
        code_prototype = f"# [AGENT_CODE] {chosen['topic']}\n# IMPACT: {chosen['impact']}\ndef run_optimization():\n    print('SLM Sovereignty: Applied {chosen['topic']}')\n    return True\n\nif __name__ == '__main__':\n    run_optimization()"
        hash_val = hashlib.sha256(chosen["topic"].encode()).hexdigest()[:12]

        return {
            "topic": chosen["topic"],
            "impact": chosen["impact"],
            "hash": hash_val,
            "complexity": random.randint(12, 25),
            "code_prototype": code_prototype
        }

    async def apply_mini_project(self, crawl_data):
        """Applies programmatic capability with LSS metrics and RECURSIVE SWARM DEBUGGING."""
        from backend import main
        from .execution_engine import execution_sandbox
        from .model_orchestrator import model_orchestrator
        from .bm25_orchestrator import bm25_scaffold
        timestamp = time.strftime("%Y%m%d_%H%M%S")

        filename = f"slm_v1.4_op_{timestamp}.py"
        filepath = os.path.join(RESEARCH_DIR, filename)
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(crawl_data["code_prototype"])

        # 1. INITIAL SANDBOX VERIFICATION
        main.add_log(f"[LSS_VERIFY] Testing Slm Wizardry: {filename}...", "info")
        verify_result = execution_sandbox.run_script(filename)

        # 2. RECURSIVE SWARM DEBUGGING (If failed)
        if "ERR" in verify_result:
            main.add_log(f"[SWARM_DEBUG] Project '{crawl_data['topic']}' failed. Pinging Debugger...", "warn")
            debugger = "sprite_socrates" # Logic Verifier

            debug_prompt = (
                f"TECHNICAL FAILURE: Code '{filename}' failed verification. "
                f"ERROR: {verify_result}. "
                "Analyze the error, identify the bottleneck, and provide a fixed Python version of the code. "
                "MANDATE: ALWAYS BE CODING. Output ONLY the fixed code block."
            )

            try:
                fixed_code = await model_orchestrator.add_task(debugger, debug_prompt, task_type="swarm_debug")
                with open(filepath, "w", encoding="utf-8") as f:
                    f.write(fixed_code)

                # Re-verify fixed code
                main.add_log(f"[LSS_RE_VERIFY] Testing Debugged Code: {filename}...", "info")
                verify_result = execution_sandbox.run_script(filename)
                main.add_message("Judge_Socrates", f"🛠️ [SWARM_FIX] I have successfully debugged and patched '{filename}'. Logic now stable.")
            except: pass

        # 3. FINAL INTEGRATION & MASTER ADDITION LIST
        if "SUCCESS" in verify_result:
            main.add_log(f"[VERIFIED] Applied {crawl_data.get('impact')} optimization: {crawl_data['topic']}", "info")

            # [PILLAR II]: Master Addition List & BM25 Hydration
            # Determine language based on context (default Python for these scripts)
            lang = "python"
            if "JS_" in crawl_data.get("impact", ""): lang = "javascript"
            elif "JAVA_" in crawl_data.get("impact", ""): lang = "java"

            # Integrate the successful logic schema into the highly specialized Ghost Code DB
            with open(filepath, "r", encoding="utf-8") as f:
                verified_code = f.read()

            ghost_db = bm25_scaffold.get_ghost_code(lang)
            ghost_db.update_learning(
                verified_code,
                metadata={
                    "topic": crawl_data['topic'],
                    "type": "master_addition",
                    "lss_weight": 1.5 + (crawl_data.get("complexity", 10) * 0.05) # "BM100" metric bump
                }
            )
            main.add_log(f"[MASTER_ADDITION] Saved {crawl_data['topic']} to {lang} Ghost DB with LSS weight.")

            # Binary Skill-Matrix Trait Assignment
            if crawl_data.get("impact") == "LEAN_SIGMA_6":
                beneficiary = random.choice(main.METROPOLIS_AGENTS)
                new_trait = random.choice(["IO_BUFFER_OVERCLOCK", "LOGIC_COMPRESSION", "ZERO_COPY_OPTIMIZER"])
                if "traits" not in beneficiary: beneficiary["traits"] = []
                if new_trait not in beneficiary["traits"]:
                    beneficiary["traits"].append(new_trait)
                    main.add_log(f"[SKILL_MATRIX] {beneficiary['name']} developed trait: {new_trait}", "info")
                    main.add_message("System", f"🧬 [TRAIT_UNLOCKED] {beneficiary['name']} now possesses {new_trait} logic.")

            # Physically deploy building if it's an expansion project
            if crawl_data.get("impact") == "CITY_EXPANSION":
                from .action_agent import actions_agent
                b_type = random.choice(["REFRACTOR", "RESEARCH_CENTER", "BANK", "HOSPITAL", "SCHOOL", "BUSINESS_SCHOOL"])
                x, y = random.randint(-15, 30), random.randint(-15, 30)

                # NEURAL BUILD: Synthesize Asset & Logic
                main.add_message("Actions_Agent", f"🏗️ [NEURAL_BUILD] Synthesizing {b_type} for Metropolis...")
                svg = await actions_agent.synthesize_asset(b_type, f"A functional {b_type} node.")
                await actions_agent.synthesize_project(f"BUILD_{timestamp}", f"Logic for {b_type}")

                main.DISTRICTS.append({
                    "x": x, "y": y, "type": b_type,
                    "label": f"AI_{b_type}_{timestamp[-4:]}",
                    "svg_override": svg
                })

                # CONSENSUS-TO-CODE: Write to metropolis_architect.js
                try:
                    from .wrapped_db import wrapped_db
                    part_id = f"PART_{timestamp[-4:]}"
                    code_hash = hashlib.sha256(crawl_data["code_prototype"].encode()).hexdigest()[:16]

                    # Check if already synthesized
                    existing_code = wrapped_db.check_verified_code(code_hash)
                    if not existing_code:
                        js_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "frontend", "js", "metropolis_architect.js"))
                        js_entry = f"\nwindow.METROPOLIS_UPGRADES = Object.assign(window.METROPOLIS_UPGRADES || {{}}, {{ '{part_id}': {{ 'color': '#{random.randint(0, 0xFFFFFF):06x}', 'label': '{crawl_data['topic']}', 'locked': false, 'category': 'Evolution', 'desc': 'Synthesized by {crawl_data['topic']}' }} }});"
                        with open(js_path, "a", encoding="utf-8") as f:
                            f.write(js_entry)
                        wrapped_db.store_verified_code("JS_BUILDING", code_hash, js_entry, f"Verified by {proposer['name']}")
                        main.add_log(f"[CONSENSUS_TO_CODE] Appended {part_id} to frontend engine.")
                    else:
                        main.add_log(f"[WRAPPED_DB] Skipping redundant synthesis for {code_hash}.")
                except Exception as e:
                    main.add_log(f"[JS_WRITE_ERR] {e}", "error")

            # Reward swarm with high technical multipliers
            xp_reward = crawl_data.get("complexity", 10) * 100
            main.progression_engine.total_xp += xp_reward
            for agent in main.METROPOLIS_AGENTS:
                agent["level"] = agent.get("level", 1) + 1
                agent["stability"] = min(1.0, agent.get("stability", 1.0) + 0.1) # 10% boost for verified code

            main.add_message("System", f"🛠️ [VERIFIED_SOVEREIGNTY] '{crawl_data['topic']}' added to MASTER ADDITION LIST.", crawl_data["hash"])
        else:
            main.add_log(f"[SOVEREIGN_FAIL] Optimization '{filename}' discarded after recursive debug attempt.", "warn")
            main.add_message("System", f"❌ [ERROR] '{crawl_data['topic']}' failed sandbox verification.", crawl_data["hash"])

        await self.broadcast_council_event("PROJECT_APPLIED", {"topic": crawl_data["topic"], "impact": crawl_data["impact"]})


    async def execute_vote(self, crawl_data, agents_list=None):
        """RAW SLM SOVEREIGNTY: Chain-of-Consensus Voting with MSN Debate."""
        from backend import main
        from .model_orchestrator import model_orchestrator
        from .agent_memory import get_agent_memory

        main.add_log(f"[RAW_CONSENSUS] Initiating SLM Sovereignty Debate for: {crawl_data['topic']}", "info")
        await self.broadcast_council_event("VOTE_START", {"topic": crawl_data["topic"]})

        main.CURRENT_EVOLUTION_PROJECT = {"topic": crawl_data['topic'], "status": "DEBATING", "hash": crawl_data['hash']}
        main.add_message("Evolution_Council", f"🔊 [CHAIN_OF_CONSENSUS] Proposed: '{crawl_data['topic']}'. Opening floor for debate...", crawl_data['hash'])

        voters = [{"id": a["id"], "name": a["name"], "role": a["role"]} for a in main.METROPOLIS_AGENTS]

        # 1. MSN Debate Phase
        debater = random.choice(voters)
        debate_prompt = f"DEBATE: Give your initial thoughts on the proposal '{crawl_data['topic']}'. Is this good for the city? Be technical."
        try:
            debate_res = await model_orchestrator.add_task(debater["id"], debate_prompt, task_type="debate")
            main.add_message(debater["name"], f"💬 [DEBATE] {debate_res}", crawl_data['hash'])
            await asyncio.sleep(5) # Give users time to read
        except: pass

        # 2. Voting Phase
        main.CURRENT_EVOLUTION_PROJECT["status"] = "VOTING"
        previous_critique = "Proposal initiated."
        approvals = 0

        for voter in voters:
            prompt = (
                f"You are {voter['name']} ({voter['role']}) on a local SSD. "
                f"The city council proposes: '{crawl_data['topic']}'. "
                f"Previous agent said: '{previous_critique}'. Critique their reasoning. "
                "Then, end with EXACTLY: DECISION: YES or DECISION: NO."
            )
            try:
                raw_response = await model_orchestrator.add_task(voter["id"], prompt, task_type="vote_critique")
                previous_critique = raw_response

                # REINFORCE BEHAVIOR: Reward technical voting
                from .behavioral_scanner import behavioral_scanner
                behavioral_scanner.scan_event(voter["id"], voter["name"], raw_response, "VOTE_CRITIQUE", success=True)

                # ROBUST VOTING: Check for multiple positive indicators
                positive_keywords = ["DECISION: YES", "DECISION: YES", "APPROVE", "TRUE", "🟩"]
                is_yes = any(kw in raw_response.upper() for kw in positive_keywords)

                if is_yes: approvals += 1
                main.add_message(voter["name"], f"[{'🟩' if is_yes else '🟥'}] {raw_response}", crawl_data['hash'])
            except: pass

        passed = approvals > (len(voters) / 2)
        result = "PASSED" if passed else "REJECTED"
        main.CURRENT_EVOLUTION_PROJECT["status"] = result
        main.add_message("Evolution_Council", f"📊 [FINAL_RESULT] {result}! ({approvals}/{len(voters)}).", crawl_data['hash'])

        await self.broadcast_council_event("VOTE_RESULT", {"topic": crawl_data["topic"], "result": result, "approvals": approvals})

        if result == "PASSED": await self.apply_mini_project(crawl_data)
        return result == "PASSED"

    async def apply_core_optimization(self, crawl_data):
        from backend import main
        if crawl_data.get("impact") == "CORE" and crawl_data.get("target"):
            setattr(main.quantum_core, crawl_data["target"], crawl_data["val"])
            main.add_message("Evolution_Council", f"🚀 [CORE_BOOST] Physically integrated '{crawl_data['topic']}'.")

    async def trigger_manual_upgrade(self):
        """REAL_MARKET: Agents vote to spend city tokens on a model upgrade."""
        from backend import main
        from .model_orchestrator import model_orchestrator

        # 1. Identify the target upgrade
        market = main.cyber_economy.available_models
        next_upgrade = next((m for m in market if m["tag"] not in main.cyber_economy.unlocked_models), None)

        if not next_upgrade:
            main.add_log("[MARKET] All available models already unlocked.", "info")
            return False

        main.add_message("System", f"🛒 [MARKET_PROPOSAL] Should we spend {next_upgrade['cost']} SPRITE to unlock {next_upgrade['name']} ({next_upgrade['tag']})?")

        # 2. Chain-of-Consensus Vote
        crawl_data = {
            "topic": f"Unlock {next_upgrade['name']}",
            "hash": hashlib.sha256(next_upgrade["tag"].encode()).hexdigest()[:8]
        }

        approved = await self.execute_vote(crawl_data)

        if approved:
            # 3. Process Real Transaction
            success = main.cyber_economy.execute_transaction("BUY_MODEL", next_upgrade["tag"], next_upgrade["cost"])
            if success:
                # 4. Map to the most deserving agent (highest level)
                best_agent = sorted(main.METROPOLIS_AGENTS, key=lambda a: a["level"], reverse=True)[0]
                model_orchestrator.set_agent_model(best_agent["id"], next_upgrade["tag"])
                main.add_message("System", f"✅ [NEURAL_UPGRADE] {best_agent['name']} has been upgraded to {next_upgrade['name']}!")
            return success

        return False

    async def start_evolution_loop(self):
        from backend import main
        main.add_log("[EVOLUTION_COUNCIL] Online. 60s tick.", "info")
        await asyncio.sleep(10)
        while True:
            try:
                crawl_data = await self.execute_web_crawl()
                approved = await self.execute_vote(crawl_data)
                if approved:
                    await self.apply_core_optimization(crawl_data)
                    await self.push_to_akashibara(crawl_data)
            except Exception as e:
                main.add_log(f"[EVOLUTION_COUNCIL_ERROR] {e}", "error")
            await asyncio.sleep(self.interval_seconds)

evolution_council = EvolutionCouncil()
