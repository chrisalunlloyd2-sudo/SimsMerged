# [TIMESTAMP: 2026-06-12T20:50:00.000Z] [PROJECT_ID: SimsMerged-v1.4.2] [AGENT_ID: viper_cli-architectssj4]
import os
import json
import time
import asyncio
from typing import List, Dict
from .config import SSD_SANDBOX_PATH, add_log, add_message
from .model_orchestrator import model_orchestrator

class IdeatorAgent:
    """
    [BLOCK 1]: HARVEST & EXTRACT (SEMANTIC EXTRACTION)
    - Parses chat logs and TODOs to extract 'Performatives'.
    - Generates a 'Task Manifest' for the Implementer.
    """
    def __init__(self):
        self.chat_log_path = os.path.join(SSD_SANDBOX_PATH, "metropolis_chat.json")
        self.task_manifest_path = os.path.join(SSD_SANDBOX_PATH, "task_manifest.json")

    async def harvest_performatives(self):
        tasks = []

        # 1. Harvest from Chat Logs (Existing)
        if os.path.exists(self.chat_log_path):
            try:
                with open(self.chat_log_path, "r", encoding="utf-8") as f:
                    chats = json.load(f)
                user_intents = [c['msg'] for c in chats if c['sender'] == 'User'][-5:]
                if user_intents:
                    prompt = (
                        f"You are the IDEATOR_AGENT. Analyze these user intents and extract tech PERFORMATIVES.\n"
                        f"CONTEXT:\n{chr(10).join(user_intents)}\n\n"
                        "Output JSON list: [{'task': '...', 'context': '...', 'dependencies': []}]"
                    )
                    res = await model_orchestrator.add_task("Ideator_Chat", prompt, task_type="ideation_harvest")
                    tasks.extend(json.loads(res))
            except: pass

        # 2. [PILLAR V] Codebase TODO Sweep
        # Recursive scan for tech debt and TODOs
        todo_context = ""
        project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
        for root, dirs, files in os.walk(project_root):
            if any(x in root for x in [".git", "node_modules", "__pycache__", "target"]): continue
            for file in files:
                if file.endswith((".py", ".java", ".js", ".ps1")):
                    path = os.path.join(root, file)
                    try:
                        with open(path, "r", encoding="utf-8") as f:
                            lines = f.readlines()
                            for i, line in enumerate(lines):
                                if any(kw in line.upper() for kw in ["TODO", "FIXME", "OPTIMIZE"]):
                                    todo_context += f"FILE: {file} L{i+1}: {line.strip()}\n"
                    except: pass

        if todo_context:
            prompt = (
                "You are the ARCHITECT_IDEATOR. Analyze these codebase TODOs and technical gaps. "
                "Generate high-resolution engineering tasks to resolve them. Ensure strict project continuity.\n\n"
                f"GAPS:\n{todo_context[:4000]}\n\n"
                "Output JSON list: [{'task': '...', 'context': '...', 'dependencies': []}]"
            )
            try:
                res = await model_orchestrator.add_task("Ideator_Audit", prompt, task_type="ideation_audit")
                tasks.extend(json.loads(res))
            except: pass

        # Save to Manifest
        if tasks:
            current_tasks = []
            if os.path.exists(self.task_manifest_path):
                with open(self.task_manifest_path, "r", encoding="utf-8") as f:
                    current_tasks = json.load(f)

            # Deduplicate and append
            for t in tasks:
                if not any(et.get("task") == t.get("task") for et in current_tasks):
                    current_tasks.append(t)

            with open(self.task_manifest_path, "w", encoding="utf-8") as f:
                json.dump(current_tasks, f, indent=2)

            add_message("Ideator", f"📋 [MANIFEST_UPDATED] Swarm generated {len(tasks)} new autonomous tasks from chat and code audit.")
            return current_tasks
        return []

class CompetencyProfile:
    """
    [PEDAGOGICAL EXPANSION]: KNOWLEDGE TRACING
    - Maintains a 'Competency Profile' for the project.
    - Identifies recurring bug classes and suggests architectural patterns.
    """
    def __init__(self):
        self.profile_path = os.path.join(SSD_SANDBOX_PATH, "competency_profile.json")
        self.profile = self._load_profile()

    def _load_profile(self):
        if os.path.exists(self.profile_path):
            with open(self.profile_path, "r", encoding="utf-8") as f:
                return json.load(f)
        return {"recurring_bugs": {}, "mastered_patterns": [], "weak_areas": []}

    def record_event(self, event_type: str, details: str):
        if event_type == "RUNTIME_FAIL":
            bug_class = details.split(":")[0]
            self.profile["recurring_bugs"][bug_class] = self.profile["recurring_bugs"].get(bug_class, 0) + 1

            if self.profile["recurring_bugs"][bug_class] > 5:
                add_message("Architect_Advisory", f"💡 [KNOWLEDGE_TRACING] Recurring bug '{bug_class}' detected 5+ times. Suggesting defensive pattern implementation.")

        self._save_profile()

    def _save_profile(self):
        with open(self.profile_path, "w", encoding="utf-8") as f:
            json.dump(self.profile, f, indent=2)

ideator = IdeatorAgent()
competency_profile = CompetencyProfile()

async def start_ideation_loop():
    """Loop for autonomous ideation and knowledge tracing."""
    add_log("🧠 Ideator Agent Online. Harvesting performatives every 15 mins.")
    while True:
        await asyncio.sleep(900)
        await ideator.harvest_performatives()
