# [TIMESTAMP: 2026-06-07T15:10:00.000Z] [PROJECT_ID: SimsMerged-v1.4.2] [AGENT_ID: Gemini-CLI-Architect]

import sqlite3
import os
import time
import json
from .config import SSD_SANDBOX_PATH

WRAPPED_DB_PATH = os.path.join(SSD_SANDBOX_PATH, "wrapped_logic.db")

class WrappedDatabase:
    """
    PERSISTENT WRAPPED LOGIC:
    - Stores successful binomial choices and verified code blocks.
    - Prevents redundant execution (Executing code/commands 2 times).
    """
    def __init__(self):
        self._init_db()

    def _init_db(self):
        conn = sqlite3.connect(WRAPPED_DB_PATH)
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS choices (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT,
                agent_id TEXT,
                question TEXT,
                choice TEXT,
                outcome TEXT
            )
        ''')
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS successful_code (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT,
                task_type TEXT,
                code_hash TEXT UNIQUE,
                code_block TEXT,
                verification_log TEXT
            )
        ''')
        conn.commit()
        conn.close()

    def record_choice(self, agent_id, question, choice, outcome="PENDING"):
        timestamp = time.strftime("%Y-%m-%dT%H:%M:%S.000Z", time.gmtime())
        conn = sqlite3.connect(WRAPPED_DB_PATH)
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO choices (timestamp, agent_id, question, choice, outcome)
            VALUES (?, ?, ?, ?, ?)
        ''', (timestamp, agent_id, question, choice, outcome))
        conn.commit()
        conn.close()

    def store_verified_code(self, task_type, code_hash, code_block, log):
        timestamp = time.strftime("%Y-%m-%dT%H:%M:%S.000Z", time.gmtime())
        conn = sqlite3.connect(WRAPPED_DB_PATH)
        cursor = conn.cursor()
        try:
            cursor.execute('''
                INSERT INTO successful_code (timestamp, task_type, code_hash, code_block, verification_log)
                VALUES (?, ?, ?, ?, ?)
            ''', (timestamp, task_type, code_hash, code_block, log))
            conn.commit()
        except sqlite3.IntegrityError:
            pass # Code already exists
        conn.close()

    def check_verified_code(self, code_hash):
        conn = sqlite3.connect(WRAPPED_DB_PATH)
        cursor = conn.cursor()
        cursor.execute('SELECT code_block FROM successful_code WHERE code_hash = ?', (code_hash,))
        row = cursor.fetchone()
        conn.close()
        return row[0] if row else None

wrapped_db = WrappedDatabase()
