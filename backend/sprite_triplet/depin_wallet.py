# TIMESTAMP: 2026-06-09
# PROJECT_ID: SimsMerged-v1.4.2
# AGENT_ID: viper_cli-architectssj4
# DESCRIPTION: Phase 4 - DePIN Wallet & Resource Gating

import sqlite3
import hashlib
import time
import uuid
import logging
import os
from contextlib import contextmanager

logger = logging.getLogger("DePIN_Wallet")
logger.setLevel(logging.INFO)

class DePINLedger:
    def __init__(self, db_path: str = r"C:\Users\viper\Desktop\SimsMerged\backend\depin_ledger.db"):
        self.db_path = db_path
        self._initialize_db()

    @contextmanager
    def get_db_connection(self):
        conn = sqlite3.connect(self.db_path, timeout=10.0)
        try:
            yield conn
        finally:
            conn.close()

    def _initialize_db(self):
        """Step 18.1: Create SQLite ledger for sovereign agent wallets."""
        with self.get_db_connection() as conn:
            conn.execute('PRAGMA journal_mode=WAL;')
            cursor = conn.cursor()
            
            # Wallets Table (Upgraded with Lifespan & DePIN Metadata)
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS wallets (
                    agent_id TEXT PRIMARY KEY,
                    address TEXT UNIQUE,
                    balance REAL DEFAULT 0.0,
                    status TEXT DEFAULT 'ACTIVE',
                    birth_timestamp REAL,
                    lifespan REAL DEFAULT 86400.0,
                    last_updated REAL
                )
            ''')
            
            # Transactions Table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS transactions (
                    tx_hash TEXT PRIMARY KEY,
                    agent_id TEXT,
                    amount REAL,
                    tx_type TEXT,
                    timestamp REAL,
                    FOREIGN KEY(agent_id) REFERENCES wallets(agent_id)
                )
            ''')
            conn.commit()

    def _generate_tx_hash(self, agent_id: str, amount: float, timestamp: float) -> str:
        """Build cryptographic token generation hash."""
        raw = f"{agent_id}:{amount}:{timestamp}:{uuid.uuid4().hex}"
        return hashlib.sha256(raw.encode('utf-8')).hexdigest()

    def generate_sovereign_address(self, agent_id: str) -> str:
        """Step 18.1: Generate unique SHA-256 non-custodial address."""
        raw = f"{agent_id}:{uuid.uuid4().hex}"
        addr = f"0x{hashlib.sha256(raw.encode('utf-8')).hexdigest()[:40]}"
        return addr

    def fund_wallet(self, agent_id: str, amount: float) -> str:
        """Step 35 / 18.1: Initialize or fund sovereign wallet."""
        timestamp = time.time()
        
        with self.get_db_connection() as conn:
            cursor = conn.cursor()
            
            # Check if address exists
            cursor.execute('SELECT address, birth_timestamp FROM wallets WHERE agent_id = ?', (agent_id,))
            row = cursor.fetchone()
            address = row[0] if row else self.generate_sovereign_address(agent_id)
            birth = row[1] if row and row[1] else timestamp
            
            # Upsert wallet
            cursor.execute('SELECT agent_id FROM wallets WHERE agent_id = ?', (agent_id,))
            if cursor.fetchone():
                cursor.execute('''
                    UPDATE wallets SET 
                    balance = balance + ?, 
                    last_updated = ?,
                    status = 'ACTIVE'
                    WHERE agent_id = ?
                ''', (amount, timestamp, agent_id))
            else:
                cursor.execute('''
                    INSERT INTO wallets (agent_id, address, balance, birth_timestamp, last_updated) 
                    VALUES (?, ?, ?, ?, ?)
                ''', (agent_id, address, amount, birth, timestamp))
            
            tx_hash = self._generate_tx_hash(agent_id, amount, timestamp)
            cursor.execute('''
                INSERT INTO transactions (tx_hash, agent_id, amount, tx_type, timestamp)
                VALUES (?, ?, ?, 'FUNDING', ?)
            ''', (tx_hash, agent_id, amount, timestamp))
            conn.commit()
            
        logger.info(f"Sovereign Wallet {address[:10]}... funded with {amount} tokens.")
        return tx_hash

    def get_agent_lifespan_data(self, agent_id: str):
        """Fetch real-time lifespan remaining for an agent."""
        with self.get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT birth_timestamp, lifespan, status, balance FROM wallets WHERE agent_id = ?', (agent_id,))
            row = cursor.fetchone()
            if not row: return None
            
            birth, lifespan, status, balance = row
            if not birth: birth = time.time()
            
            elapsed = time.time() - birth
            remaining = lifespan - elapsed
            
            return {
                "birth": birth,
                "lifespan": lifespan,
                "elapsed": elapsed,
                "remaining": remaining,
                "status": status,
                "balance": balance
            }

    def extend_lifespan(self, agent_id: str, hours: float = 24.0) -> bool:
        """Extend agent lifespan by spending tokens (100 tokens per 24h)."""
        cost = (hours / 24.0) * 100.0
        extension_seconds = hours * 3600.0
        
        if self._burn_tokens(agent_id, cost, "LIFESPAN_EXTENSION"):
            with self.get_db_connection() as conn:
                cursor = conn.cursor()
                cursor.execute('UPDATE wallets SET lifespan = lifespan + ? WHERE agent_id = ?', (extension_seconds, agent_id))
                conn.commit()
            return True
        return False

    def get_all_lifespan_stats(self):
        """Returns stats for all agents for the Metropolis Vision grade."""
        stats = {}
        with self.get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT agent_id FROM wallets')
            agents = [r[0] for r in cursor.fetchall()]
            for aid in agents:
                stats[aid] = self.get_agent_lifespan_data(aid)
        return stats

    def charge_compute_fee(self, agent_id: str, cpu_seconds: float) -> bool:
        """Step 18.3: Compute Budget Engine (Micro-cent billing)."""
        # Cost: 0.0001 tokens per CPU second
        cost = cpu_seconds * 0.0001
        return self._burn_tokens(agent_id, cost, "COMPUTE_BILLING")

    def _burn_tokens(self, agent_id: str, cost: float, tx_type: str) -> bool:
        timestamp = time.time()
        tx_hash = self._generate_tx_hash(agent_id, -cost, timestamp)
        
        with self.get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('BEGIN EXCLUSIVE TRANSACTION;')
            
            cursor.execute('SELECT balance, address FROM wallets WHERE agent_id = ?', (agent_id,))
            row = cursor.fetchone()
            
            if not row or row[0] < cost:
                cursor.execute('UPDATE wallets SET status = "SUSPENDED" WHERE agent_id = ?', (agent_id,))
                conn.commit()
                logger.warning(f"Sovereign Breach: {agent_id} has insufficient funds for {tx_type}.")
                return False
                
            cursor.execute('''
                UPDATE wallets SET balance = balance - ?, last_updated = ? WHERE agent_id = ?
            ''', (cost, timestamp, agent_id))
            
            cursor.execute('''
                INSERT INTO transactions (tx_hash, agent_id, amount, tx_type, timestamp)
                VALUES (?, ?, ?, ?, ?)
            ''', (tx_hash, agent_id, -cost, tx_type, timestamp))
            
            conn.commit()
            
        logger.info(f"Burned {cost:.6f} tokens for {tx_type}. Agent: {agent_id}")
        return True

    def charge_inference_fee(self, agent_id: str, context_length: int) -> bool:
        """Legacy Sprite charge logic updated to use burn."""
        cost = max(0.01, context_length * 0.0001)
        return self._burn_tokens(agent_id, cost, "INFERENCE_BURN")

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    ledger = DePINLedger()
    
    agent = "L3_SMOLL_01"
    
    # Tok Tree funds agent
    ledger.fund_wallet(agent, 5.0)
    
    # Agent executes a query with 4096 context
    success = ledger.charge_inference_fee(agent, 4096)
    print(f"Execution 1 Allowed: {success}")
    
    # Drain wallet quickly
    ledger.charge_inference_fee(agent, 50000)
    ledger.charge_inference_fee(agent, 50000)
    
    # Agent attempts execution without funds
    success_fail = ledger.charge_inference_fee(agent, 1024)
    print(f"Execution Allowed after drain: {success_fail}")
