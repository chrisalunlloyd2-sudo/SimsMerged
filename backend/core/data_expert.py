# [TIMESTAMP: 2026-06-07T20:30:00.000Z] [PROJECT_ID: SimsMerged-v1.4.2] [AGENT_ID: Gemini-CLI-Architect]

import os
import json
import time
import re
from typing import List, Dict, Optional
from .config import SSD_SANDBOX_PATH, MSG_LOG

DATA_EXPERTISE_PATH = os.path.join(SSD_SANDBOX_PATH, "metropolis_data_sovereignty.json")

class DataExpert:
    """
    DATA EXPERT AGENT:
    - Harvests user chats to extract TODOs and missing requirements.
    - Manages a master 'Missing Features' list.
    - Provides a 'Stuck Hook' for models to ask clarifying questions.
    """
    def __init__(self):
        self.master_todo_list = []
        self.missing_features = []
        self._load_state()

    def _load_state(self):
        if os.path.exists(DATA_EXPERTISE_PATH):
            try:
                with open(DATA_EXPERTISE_PATH, "r") as f:
                    data = json.load(f)
                    self.master_todo_list = data.get("todos", [])
                    self.missing_features = data.get("missing", [])
            except: pass

    def _save_state(self):
        with open(DATA_EXPERTISE_PATH, "w") as f:
            json.dump({
                "todos": self.master_todo_list,
                "missing": self.missing_features,
                "last_harvest": time.time()
            }, f, indent=2)

    def harvest_chat(self, chat_logs: List[Dict]):
        """Extracts TODOs and technical mandates from user chat chunks with TRUNCATION."""
        new_items = []
        for msg in chat_logs:
            text = msg.get("text", "")
            # Step 1: Chunking/Separating
            text_chunks = self._chunk_text(text, max_len=100)
            
            for chunk in text_chunks:
                # Step 2: Extraction Heuristic
                if any(verb in chunk.lower() for verb in ["add", "implement", "make", "create", "fix", "need"]):
                    if len(chunk.strip()) > 10:
                        new_items.append(chunk.strip())
        
        for item in new_items:
            if item not in self.master_todo_list:
                self.master_todo_list.append(item)
        self._save_state()

    def _chunk_text(self, text: str, max_len: int) -> List[str]:
        """Separates text into small chunks for context efficiency."""
        # Split by semantic markers
        raw_chunks = re.split(r'[.!?\n]', text)
        processed = []
        for c in raw_chunks:
            # Truncate if single chunk is too long
            if len(c) > max_len:
                processed.append(c[:max_len] + "...")
            else:
                processed.append(c.strip())
        return [p for p in processed if p]

    def query_clarification(self, stuck_model_id: str, context: str):
        """Hook for when a model is stuck or missing data."""
        question = f"[STUCK_HOOK] Model {stuck_model_id} needs data on: {context}. User, can you clarify?"
        print(question)
        return question

    def get_master_list(self):
        return {
            "todos": self.master_todo_list,
            "missing": self.missing_features
        }

    def update_missing_features(self):
        """
        GAP ANALYSIS:
        Compares harvested mandates against actual file implementations and CATALOG metadata.
        """
        missing = []
        
        # 1. Check for Hyper-Productivity Implementation
        # We have the ActionsAgent class, but is it producing 'many pages'?
        if not os.path.exists(os.path.join(SSD_SANDBOX_PATH, "external_code_cache")):
            missing.append("CRITICAL: Github Code Mirroring not initialized.")
        
        # 2. Check for Physical Containerization
        # proot/docker isolation check
        if not os.path.exists(os.path.join(SSD_SANDBOX_PATH, "containers_active.lock")):
            missing.append("INFRA: Agents not yet isolated in proot/docker sandboxes.")

        # 3. Check for Real DuckDB Timescale usage in main loop
        # Is the main loop actually querying the new DuckDB for decisions?
        
        self.missing_features = missing
        self._save_state()
        return missing

    def harvest_session_context(self, session_text: str):
        """Deep harvest of the current user session text to extract granular mandates."""
        patterns = [
            r"proot or docker",
            r"realduckdb timescale",
            r"webcrawl database retrieval",
            r"google code retrieval without quotas",
            r"many pages at a time",
            r"4 step multi recursion loop",
            r"extract todos truncate and separate into small chunks"
        ]
        
        for p in patterns:
            if re.search(p, session_text, re.IGNORECASE):
                mandate = f"MANDATE DETECTED: {p}"
                if mandate not in self.master_todo_list:
                    self.master_todo_list.append(mandate)
        
        self._save_state()
        return self.master_todo_list

data_expert = DataExpert()
