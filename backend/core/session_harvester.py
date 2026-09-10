# [TIMESTAMP: 2026-06-08T04:30:00.000Z] [PROJECT_ID: SimsMerged-v1.4.2] [AGENT_ID: viper_cli-architectssj4]

import os
import json
import re
from typing import List, Dict

MASTER_TODO_PATH = "C:\\Users\\viper\\Desktop\\SimsMerged\\SSD_SANDBOX\\master_todo_list.json"

class SessionHarvester:
    """
    SESSION HARVESTER:
    - Extracts granular mandates from user chat context.
    - Separates large requests into small, actionable chunks.
    - Maintains the Master TODO list across sessions.
    """
    def __init__(self):
        self.todos = self._load_todos()

    def _load_todos(self):
        if os.path.exists(MASTER_TODO_PATH):
            with open(MASTER_TODO_PATH, "r") as f:
                return json.load(f)
        return []

    def harvest_mandates(self, session_context: str):
        """Regex-based extraction of technical requirements."""
        patterns = [
            r"proot or docker",
            r"realduckdb timescale",
            r"many pages at a time",
            r"4 step multi recursion loop",
            r"real cpu stats",
            r"agent tool panel",
            r"mass deploy",
            r"throttle agents",
            r"neural profiling",
            r"role reassignment"
        ]

        extracted = []
        for p in patterns:
            if re.search(p, session_context, re.IGNORECASE):
                extracted.append(f"MANDATE: {p.upper()}")

        # Merge and dedup
        for item in extracted:
            if item not in self.todos:
                self.todos.append(item)

        self._save_todos()
        return extracted

    def _save_todos(self):
        with open(MASTER_TODO_PATH, "w") as f:
            json.dump(self.todos, f, indent=2)

harvester = SessionHarvester()

# HARVESTING CURRENT SESSION
context = """
make clippy actually have power over agents and able to throttle agents too
many pages at a time based on a vector db retreival scema and a table the model simple picks and chooses in a 4 step multi recursion loop
clippy actually have power over agents and able to throttle agents too
real agents real cpu stats real raM STATS REAL HDD STATS
"""
harvester.harvest_mandates(context)
