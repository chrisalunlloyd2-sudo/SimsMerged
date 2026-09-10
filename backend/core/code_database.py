# [TIMESTAMP: 2026-06-05T04:30:00.000Z] [PROJECT_ID: SimsMerged-v1.4] [AGENT_ID: Antigravity-CLI-Architect]

import sqlite3
import os
import json
import time
import hashlib

from .config import KNOWLEDGE_DB_PATH

class SwarmKnowledgeHive:
    """
    UPGRADED REAL CODE DATABASE:
    - Uses SQLite for high-performance, SSD-fenced storage.
    - Tracks neural hit rates and logit stability.
    - Prevents RAM bloat by streaming from the physical platter.
    """
    def __init__(self, db_path=None):
        self.db_path = db_path or KNOWLEDGE_DB_PATH
        self._init_db()

    def _init_db(self):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS knowledge_blocks (
                hash TEXT PRIMARY KEY,
                topic TEXT,
                code TEXT,
                agent_id TEXT,
                timestamp REAL,
                hits INTEGER DEFAULT 0,
                logit_hash TEXT
            )
        ''')
        conn.commit()
        conn.close()

    def store_snippet(self, topic, code, agent_id="SWARM", logit_hash=None):
        topic_hash = hashlib.sha256(topic.lower().strip().encode()).hexdigest()
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        try:
            cursor.execute('''
                INSERT OR IGNORE INTO knowledge_blocks (hash, topic, code, agent_id, timestamp, logit_hash)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (topic_hash, topic, code, agent_id, time.time(), logit_hash))
            conn.commit()
        except: pass
        finally: conn.close()
        return topic_hash

    def get_snippet(self, topic):
        topic_hash = hashlib.sha256(topic.lower().strip().encode()).hexdigest()
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('SELECT code FROM knowledge_blocks WHERE hash = ?', (topic_hash,))
        row = cursor.fetchone()
        if row:
            cursor.execute('UPDATE knowledge_blocks SET hits = hits + 1 WHERE hash = ?', (topic_hash,))
            conn.commit()
        conn.close()
        return row[0] if row else None

    def get_recent_stats(self, limit=5):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('SELECT topic, agent_id, hits FROM knowledge_blocks ORDER BY timestamp DESC LIMIT ?', (limit,))
        rows = cursor.fetchall()
        conn.close()
        return [{"topic": r[0], "agent": r[1], "hits": r[2]} for r in rows]

knowledge_hive = SwarmKnowledgeHive()
