# [TIMESTAMP: 2026-06-11T04:50:00.000Z] [PROJECT_ID: SimsMerged-v1.4.2] [AGENT_ID: Gemini-CLI-Architect]

import os
import duckdb
import json
from .config import SSD_SANDBOX_PATH

GOOD_CODE_DB_PATH = os.path.join(SSD_SANDBOX_PATH, "good_code.duckdb")

class GoodCodeDatabase:
    """
    PHASE 31: THE GOOD CODE DATABASE (RAG LAYER)
    - Stores high-quality, verified code snippets.
    - Used as the knowledge source for the Predictive Engine.
    """
    def __init__(self):
        self.conn = duckdb.connect(GOOD_CODE_DB_PATH)
        self._initialize()

    def _initialize(self):
        self.conn.execute("CREATE SEQUENCE IF NOT EXISTS seq_good_code_id")
        self.conn.execute("""
            CREATE TABLE IF NOT EXISTS good_code (
                id INTEGER PRIMARY KEY DEFAULT nextval('seq_good_code_id'),
                language VARCHAR,
                category VARCHAR,
                code TEXT,
                tags JSON,
                quality_score FLOAT,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

    def insert_code(self, language: str, category: str, code: str, tags: list, score: float = 1.0):
        self.conn.execute(
            "INSERT INTO good_code (language, category, code, tags, quality_score) VALUES (?, ?, ?, ?, ?)",
            (language, category, code, json.dumps(tags), score)
        )

    def search_code(self, query: str, language: str = None) -> list:
        # Simple keyword search as a RAG baseline
        where = f"WHERE code LIKE '%{query}%'"
        if language:
            where += f" AND language = '{language}'"

        results = self.conn.execute(f"SELECT code, category, tags FROM good_code {where} ORDER BY quality_score DESC LIMIT 5").fetchall()
        return [{"code": r[0], "category": r[1], "tags": json.loads(r[2])} for r in results]

good_code_db = GoodCodeDatabase()
