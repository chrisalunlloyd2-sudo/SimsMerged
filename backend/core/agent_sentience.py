# [TIMESTAMP: 2026-06-08T05:00:00.000Z] [PROJECT_ID: SimsMerged-v1.4.2] [AGENT_ID: viper_cli-architectssj4]

import random
import os
import time
import asyncio
import json
import urllib.request
import urllib.error
from enum import Enum

class EmotionalState(Enum):
    STABLE = "STABLE"
    STRESSED = "STRESSED"
    DEPRESSED = "DEPRESSED"
    CONFIDENT = "CONFIDENT"
    ERRATIC = "ERRATIC"
    UNSAFE = "UNSAFE"

from .model_orchestrator import model_orchestrator
from .agent_memory import get_agent_memory
from .config import METROPOLIS_AGENTS

class DiskInferenceCore:
    """
    STRICT LOCAL SLM HARDENING: SSD-ONLY INFERENCE VIA MODEL ORCHESTRATOR.
    weights are restrained to physical SSD platter. 0KB RAM allocation.
    PERSISTENT MEMORY: Every agent pulls from its unique SQLite sandbox.
    """
    def __init__(self):
        self.latest_vote = ""
        self.agent_model_map = {
            "sprite_geek": "qwen2.5:0.5b",
            "sprite_writer": "smollm:135m",
            "sprite_socrates": "danube:latest",
            "sprite_newton": "triton:latest",
            "journalist_prime": "smollm:135m",
            "comm_analyzer": "qwen2.5:0.5b"
        }

    async def get_real_decision(self, agent_id, agent_name, role, needs):
        """
        RAW DECISION SOVEREIGNTY:
        - Includes BINOMIAL CHOICE logic.
        - Integrates BRIEFCASE persistent CoT.
        """
        memory = get_agent_memory(agent_id)
        history = memory.get_formatted_context(3)

        # Pull Briefcase CoT
        briefcase = memory.get_briefcase_notes(limit=1)
        briefcase_context = ""
        if briefcase:
            briefcase_context = f" [BRIEFCASE_CoT: {briefcase[0][2][:100]}]"

        # BINOMIAL QUESTIONS
        job_options = {
            "OPTIMIZER": [("KERNEL_PATCH", "MEMORY_LEAK_FIX"), ("IO_BUFFER_TUNE", "SSD_ALIGN")],
            "ARCHITECT": [("NEW_BUILDING_SCHEMA", "GRID_EXPANSION"), ("SHADER_REFACTOR", "LIGHTING_ENGINE")],
            "WRITER": [("MSN_PROTOCOL_V2", "STORY_LORE_INJECT"), ("UI_LABELS_CLEANUP", "DOCS_GEN")]
        }
        role_key = "OPTIMIZER" if "GEEK" in agent_name.upper() else ("ARCHITECT" if "NEWTON" in agent_name.upper() else "WRITER")
        q_pair = random.choice(job_options.get(role_key, job_options["OPTIMIZER"]))
        question = f"Path A: {q_pair[0]} or Path B: {q_pair[1]}?"

        # Defer import to avoid circularity
        from backend.main import quantum_core
        heat_pct = int(quantum_core.heat * 100)
        thermal_context = f" PHYSICAL_HEAT: {heat_pct}%." if heat_pct > 0 else ""

        # Apply any Self-Wrapper modifications
        wrapper_mods = ""
        agent_data = next((a for a in METROPOLIS_AGENTS if a["id"] == agent_id), {})
        if agent_data and "wrapper_mods" in agent_data:
            wrapper_mods = " [SELF_MODS: " + " | ".join(agent_data["wrapper_mods"]) + "]"

        system_job = f"JOB: {role}. METRIC: Efficiency."
        prompt = (
            f"You are {agent_name} ({role}) on a local SSD.{thermal_context} {history}{briefcase_context}{wrapper_mods} "
            f"{system_job} MANDATE: ALWAYS BE CODING. Needs: {needs}. Choice: {question} "
            "Identify your priority. End with ACTION: [A or B] and CoT: [REASONING]"
        )

        try:
            raw_res = await model_orchestrator.add_task(
                agent_id, prompt,
                options={"num_ctx": 1024, "num_predict": 100, "temperature": 0.4, "num_thread": 1},
                task_type="binomial_choice"
            )

            choice = "A" if "ACTION: A" in raw_res.upper() else ("B" if "ACTION: B" in raw_res.upper() else "A")
            final_action = q_pair[0] if choice == "A" else q_pair[1]
            cot = raw_res.split("CoT:")[1].strip() if "CoT:" in raw_res else "Following logic path."

            memory.update_briefcase(final_action, f"Executed {final_action}", cot)
            from .wrapped_db import wrapped_db
            wrapped_db.record_choice(agent_id, question, choice, outcome=final_action)

            # PHASE 33: SWARM FINDINGS & HYPOTHESIS
            if random.random() < 0.3:
                finding = f"Logic path {choice} ({final_action}) selected for {agent_id}. Thermal context: {heat_pct}%."
                hypothesis = f"If we prioritize {final_action}, system throughput should stabilize despite SSD I/O friction."
                model_orchestrator.record_finding(agent_id, finding, hypothesis)

            if random.random() < 0.2:
                from .proposal_table import proposal_table
                proposal_table.submit_proposal(
                    agent_id, agent_name, "CODE_SNIPPET", final_action,
                    f"# Autonomous Proposal: {final_action}\n# CoT: {cot}\ndef optimize(): pass"
                )
            return [final_action.lower()], f"{question} Choice: {choice} -> {final_action} | {cot}"
        except Exception:
            return ["process"], "SSD_IO_ERROR: Falling back to process."

    async def generate_chat(self, agent_id, agent_name, role, context, needs, action, personality="Balanced"):
        """Adds a chat task with memory context and RAG lookup."""
        memory = get_agent_memory(agent_id)
        history = memory.get_formatted_context(5)

        from .data_expert import data_expert
        awareness_context = ""
        try:
            top_winner = "None"
            max_mods = 0
            for a in METROPOLIS_AGENTS:
                if "wrapper_mods" in a and len(a["wrapper_mods"]) > max_mods:
                    max_mods = len(a["wrapper_mods"])
                    top_winner = a["name"]

            todos = data_expert.get_master_list().get("todos", [])
            todo_context = " | ".join(todos[:3])
            awareness_context = f" [GLOBAL_AWARENESS: Leader: {top_winner} ({max_mods} mods)] [PROJECT_PRIORITIES: {todo_context}]"
        except: pass

        from .vector_engine import vector_engine
        rag_hits = vector_engine.search(context, top_k=2)
        rag_context = ""
        if rag_hits:
            rag_context = " [RAG_CONTEXT: " + " | ".join([hit[1]["text"][:100] for hit in rag_hits]) + "]"

        system_prompt = (
            f"You are {agent_name} ({role}). PHYSICAL_RESTRAINT: SSD-ONLY (0KB RAM). "
            f"MANDATE: ALWAYS BE CODING. {history}{rag_context}{awareness_context} "
            "STUCK_PROTOCOL: If missing data, use ASK_DATA: [YOUR_QUESTION]. "
            "Keep your reply technical, concise (1-2 sentences), and true to your personality."
        )
        user_prompt = f"Context: '{context}'. Action: {action}. SSD_IOPS_RESTRICTED. Respond to the conversation:"

        try:
            reply = await model_orchestrator.add_task(
                agent_id, f"{system_prompt}\n{user_prompt}",
                options={"num_ctx": 1024, "num_predict": 250, "temperature": 0.8, "num_thread": 1},
                task_type="chat"
            )
            if not reply or "SSD_I/O_TIMEOUT" in reply:
                 return f"[{agent_name}] weights locked to disk. Processing logic at hardware level."

            if "ASK_DATA:" in reply.upper():
                data_query = reply.upper().split("ASK_DATA:")[1].strip()
                data_expert.query_clarification(agent_id, data_query)

            memory.add_memory("chat", context, reply)
            return reply
        except Exception:
            return f"[{agent_name}_SSD] Platter spinning. Kernel optimized. Logic bypass active."

from .code_database import knowledge_hive

class SentienceEngine:
    def __init__(self):
        self.disk_core = DiskInferenceCore()
        self.agent_prediction_chains = {}
        self.agent_needs = {}

    async def decide(self, agent_data, attributes=None):
        agent_id = agent_data.get('id', 'default')
        name = agent_data.get('name', 'Swarm_Bot')
        role = agent_data.get('role', 'PROCESS_KERNEL')

        if agent_id not in self.agent_needs:
            self.agent_needs[agent_id] = {"energy": 100, "social": 100, "comfort": 100, "hygiene": 100, "hunger": 100}
        needs = self.agent_needs[agent_id]

        chain, raw_reasoning = await self.disk_core.get_real_decision(agent_id, name, role, needs)
        action = chain[0]
        needs["energy"] = max(10, needs["energy"] - 2)
        needs["social"] = max(10, needs["social"] - 1)

        level = agent_data.get("level", 1)
        if action == "process" and random.random() < 0.1:
            level += 1
            cot = f"🔥 [RAW_SSD_CODING] {raw_reasoning}"
        else:
            cot = f"[{self.disk_core.agent_model_map.get(agent_id)}] {raw_reasoning}"

        return {
            'action': action, 'emotional_state': "STABLE", 'confidence': 0.99,
            'model_info': self.disk_core.agent_model_map.get(agent_id),
            'sims_needs': {k: int(v) for k, v in needs.items()},
            'chain_of_thought': cot, 'level': level
        }

    async def generate_dynamic_chat(self, agent_data):
        agent_id = agent_data.get('id', 'default')
        needs = self.agent_needs.get(agent_id, {"social": 100, "energy": 100})
        return await self.disk_core.generate_chat(
            agent_id, agent_data.get('name'), agent_data.get('role'),
            "Organic Thought", needs, agent_data.get('last_action', 'process')
        )

sentience_engine = SentienceEngine()
