# TIMESTAMP: 2026-06-03T21:00:00.000Z
# PROJECT_ID: SimsMerged-v1.4-Metropolis
# AGENT_ID: Gemini-CLI-Architect

import sqlite3
import os
import time
import json

from .config import AGENT_MEMORIES_DIR

class AgentMemory:
    """
    Persistent SQLite-based rolling memory for local agents.
    RESTRAINED: All databases are physically fenced to the SSD_SANDBOX.
    """
    def __init__(self, agent_id):
        self.agent_id = agent_id
        self.base_dir = AGENT_MEMORIES_DIR
        self.db_path = os.path.join(self.base_dir, f"{agent_id}.db")
        self._init_db()

    def get_formatted_context(self, limit=5):
        """
        NEURAL CONTEXT STUBBING:
        - Utilizes LLSTM pattern with BM25 long-term retrieval.
        - TRAIT_BUFF: LOGIC_COMPRESSION doubles recall capacity.
        """
        from .config import METROPOLIS_AGENTS
        agent = next((a for a in METROPOLIS_AGENTS if a["id"] == self.agent_id), None)
        if agent and "LOGIC_COMPRESSION" in agent.get("traits", []):
            limit *= 2 # Achievement-based context expansion
            
        from .llstm_bm25 import LLSTMDatabase
        llstm = LLSTMDatabase(self.agent_id)
        
        # We pass a generic query "agent action" to pull recent BM25 vectors
        return llstm.retrieve_llstm_context("coding process action", short_term_limit=limit, long_term_limit=2)

    def _init_db(self):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS memories (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT,
                action TEXT,
                context TEXT,
                response TEXT,
                metadata TEXT
            )
        ''')
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS briefcase (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT,
                topic TEXT,
                notes TEXT,
                cot_chain TEXT
            )
        ''')
        conn.commit()
        conn.close()

    def update_briefcase(self, topic, notes, cot_chain):
        timestamp = time.strftime("%Y-%m-%dT%H:%M:%S.000Z", time.gmtime())
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        # Upsert-like behavior: update if topic exists, else insert
        cursor.execute('SELECT id FROM briefcase WHERE topic = ?', (topic,))
        row = cursor.fetchone()
        if row:
            cursor.execute('UPDATE briefcase SET notes = ?, cot_chain = ?, timestamp = ? WHERE id = ?', (notes, cot_chain, timestamp, row[0]))
        else:
            cursor.execute('INSERT INTO briefcase (timestamp, topic, notes, cot_chain) VALUES (?, ?, ?, ?)', (timestamp, topic, notes, cot_chain))
        conn.commit()
        conn.close()

    def get_briefcase_notes(self, limit=3):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('SELECT topic, notes, cot_chain FROM briefcase ORDER BY id DESC LIMIT ?', (limit,))
        rows = cursor.fetchall()
        conn.close()
        return rows

    def add_memory(self, action, context, response, metadata=None):
        timestamp = time.strftime("%Y-%m-%dT%H:%M:%S.000Z", time.gmtime())
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO memories (timestamp, action, context, response, metadata)
            VALUES (?, ?, ?, ?, ?)
        ''', (timestamp, action, context, response, json.dumps(metadata) if metadata else None))
        conn.commit()
        conn.close()

    def get_rolling_memory(self, limit=10):
        """Retrieves the last N memories to form a rolling context window."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('''
            SELECT action, context, response FROM memories
            ORDER BY id DESC LIMIT ?
        ''', (limit,))
        rows = cursor.fetchall()
        conn.close()
        
        # Return in chronological order
        return rows[::-1]

    def search_memories(self, query, limit=3):
        """Simple keyword-based search for 'RAG' on local memories."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        # Very basic search, could be improved with BM25 or FTS5
        cursor.execute('''
            SELECT action, context, response FROM memories
            WHERE context LIKE ? OR response LIKE ?
            ORDER BY id DESC LIMIT ?
        ''', (f'%{query}%', f'%{query}%', limit))
        rows = cursor.fetchall()
        conn.close()
        return rows

def get_agent_memory(agent_id):
    return AgentMemory(agent_id)
