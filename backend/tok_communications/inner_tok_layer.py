# TIMESTAMP: 2026-06-09
# PROJECT_ID: SimsMerged-v1.4.2
# AGENT_ID: viper_cli-architectssj4
# DESCRIPTION: Section B, Phase 2 - Inner Tok Layer (Eavesdropping Daemon)

import sqlite3
import json
import logging
from contextlib import contextmanager

logger = logging.getLogger("InnerTok")
logger.setLevel(logging.INFO)

class InnerTokDaemon:
    def __init__(self, db_path: str = r"C:\Users\viper\Desktop\SimsMerged\backend\inner_tok.db"):
        self.db_path = db_path
        self._initialize_db()

    @contextmanager
    def get_db_connection(self):
        conn = sqlite3.connect(self.db_path, timeout=5.0)
        try:
            yield conn
        finally:
            conn.close()

    def _initialize_db(self):
        """Step 15: Store inner monologues in separate SQLite table."""
        with self.get_db_connection() as conn:
            conn.execute('PRAGMA journal_mode=WAL;')
            cursor = conn.cursor()
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS inner_monologue (
                    log_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    agent_id TEXT,
                    topological_zone TEXT,
                    raw_payload TEXT,
                    conversational_translation TEXT,
                    sentiment TEXT,
                    timestamp REAL
                )
            ''')
            conn.commit()

    def _analyze_sentiment(self, payload: str) -> str:
        """Step 19: Build sentiment analysis on agent frustration (Mocked for speed)."""
        if "error" in payload.lower() or "failed" in payload.lower():
            return "FRUSTRATED"
        if "success" in payload.lower() or "completed" in payload.lower():
            return "CONFIDENT"
        return "NEUTRAL"

    def intercept_payload(self, agent_id: str, zone: str, raw_json: dict, timestamp: float):
        """Steps 12 & 14: Hook into JSON payloads and map to conversational analogies."""
        payload_str = json.dumps(raw_json)
        sentiment = self._analyze_sentiment(payload_str)

        # Conversational Translation (Simulating LLM summarization pipeline Step 13)
        if "generate" in raw_json.get("action", ""):
            translation = f"{agent_id} is thinking about {raw_json.get('target', 'something')}..."
        elif sentiment == "FRUSTRATED":
            translation = f"{agent_id} cursed at the console. A bug was found."
        else:
            translation = f"{agent_id} performed action: {raw_json.get('action', 'unknown')}."

        with self.get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO inner_monologue
                (agent_id, topological_zone, raw_payload, conversational_translation, sentiment, timestamp)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (agent_id, zone, payload_str, translation, sentiment, timestamp))
            conn.commit()

        logger.info(f"[EAVESDROP | {sentiment}] {translation}")

if __name__ == "__main__":
    import time
    logging.basicConfig(level=logging.INFO)
    daemon = InnerTokDaemon()

    # Simulate L3 making an API call that fails
    mock_payload_fail = {"action": "compile_script", "target": "wood_gather.py", "status": "error: syntax invalid"}
    daemon.intercept_payload("L3_MINER", "ZONE_0_0_0", mock_payload_fail, time.time())

    # Simulate L2 generating an idea
    mock_payload_think = {"action": "generate_architecture", "target": "cabin layout"}
    daemon.intercept_payload("L2_ORCHESTRATOR", "ZONE_5_5_0", mock_payload_think, time.time())
