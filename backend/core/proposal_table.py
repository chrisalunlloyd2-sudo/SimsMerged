# [TIMESTAMP: 2026-06-07T16:15:00.000Z] [PROJECT_ID: SimsMerged-v1.4.2] [AGENT_ID: Gemini-CLI-Architect]

import sqlite3
import os
import time
import json
from .config import SSD_SANDBOX_PATH

PROPOSAL_DB_PATH = os.path.join(SSD_SANDBOX_PATH, "proposal_table.db")

class ProposalTable:
    """
    HEADLESS PROPOSAL TABLE:
    - Agents submit technical proposals (code, schema, features).
    - 'Slow Agent' (Auditor) ticks off proposals after verification.
    """
    def __init__(self):
        self._init_db()

    def _init_db(self):
        conn = sqlite3.connect(PROPOSAL_DB_PATH)
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS proposals (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT,
                agent_id TEXT,
                agent_name TEXT,
                type TEXT,
                topic TEXT,
                code_block TEXT,
                status TEXT DEFAULT 'PENDING',
                audit_log TEXT,
                is_safe INTEGER DEFAULT 0,
                aligns_with_project INTEGER DEFAULT 0
            )
        ''')
        conn.commit()
        conn.close()

    def submit_proposal(self, agent_id, agent_name, prop_type, topic, code):
        timestamp = time.strftime("%Y-%m-%dT%H:%M:%S.000Z", time.gmtime())
        conn = sqlite3.connect(PROPOSAL_DB_PATH)
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO proposals (timestamp, agent_id, agent_name, type, topic, code_block)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (timestamp, agent_id, agent_name, prop_type, topic, code))
        conn.commit()
        conn.close()
        return cursor.lastrowid

    def get_pending_proposals(self, limit=5):
        conn = sqlite3.connect(PROPOSAL_DB_PATH)
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM proposals WHERE status = "PENDING" ORDER BY id ASC LIMIT ?', (limit,))
        rows = cursor.fetchall()
        conn.close()
        return rows

    def update_status(self, prop_id, status, audit_log, is_safe, aligns):
        conn = sqlite3.connect(PROPOSAL_DB_PATH)
        cursor = conn.cursor()
        cursor.execute('''
            UPDATE proposals
            SET status = ?, audit_log = ?, is_safe = ?, aligns_with_project = ?
            WHERE id = ?
        ''', (status, audit_log, 1 if is_safe else 0, 1 if aligns else 0, prop_id))
        conn.commit()
        conn.close()

proposal_table = ProposalTable()
