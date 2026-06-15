# TIMESTAMP: 2026-06-09
# PROJECT_ID: SimsMerged-v1.4.2
# AGENT_ID: viper_cli-architectssj4
# DESCRIPTION: Phase 5 - Script Pyramid Integration & Sandbox

import sqlite3
import subprocess
import time
import os
import logging
from contextlib import contextmanager
import hashlib

logger = logging.getLogger("ScriptPyramid")
logger.setLevel(logging.INFO)

class ScriptPyramid:
    def __init__(self, db_path: str = r"C:\Users\viper\Desktop\SimsMerged\backend\script_pyramid.db", sandbox_dir: str = r"C:\Users\viper\Desktop\SimsMerged\SANDBOX"):
        self.db_path = db_path
        self.sandbox_dir = sandbox_dir
        if not os.path.exists(self.sandbox_dir):
            os.makedirs(self.sandbox_dir, exist_ok=True)
        self._initialize_db()

    @contextmanager
    def get_db_connection(self):
        conn = sqlite3.connect(self.db_path, timeout=10.0)
        try:
            yield conn
        finally:
            conn.close()

    def _initialize_db(self):
        with self.get_db_connection() as conn:
            conn.execute('PRAGMA journal_mode=WAL;')
            cursor = conn.cursor()
            
            # Pyramid Scripts Table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS scripts (
                    script_hash TEXT PRIMARY KEY,
                    script_name TEXT,
                    code_payload TEXT,
                    language TEXT DEFAULT 'python',
                    success_rate REAL DEFAULT 1.0,
                    execution_count INTEGER DEFAULT 0,
                    last_executed REAL
                )
            ''')
            conn.commit()

    def submit_script(self, script_name: str, code_payload: str, language: str = 'python'):
        """Steps 41 & 49: Submit a vetted script to the Pyramid DB."""
        script_hash = hashlib.sha256(code_payload.encode('utf-8')).hexdigest()
        with self.get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT OR IGNORE INTO scripts (script_hash, script_name, code_payload, language)
                VALUES (?, ?, ?, ?)
            ''', (script_hash, script_name, code_payload, language))
            conn.commit()
        logger.info(f"Script '{script_name}' integrated into Pyramid. Hash: {script_hash[:8]}")
        return script_hash

    def execute_in_sandbox(self, script_hash: str, timeout_seconds: int = 5):
        """
        Steps 43, 44, 45, 46: 
        Terminal emulation sandbox. Routes stdout/stderr back. 
        Implements infinite loop circuit breakers via timeout.
        """
        with self.get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT code_payload, language, script_name FROM scripts WHERE script_hash = ?', (script_hash,))
            row = cursor.fetchone()
            
        if not row:
            logger.error(f"Script hash {script_hash} not found in Pyramid.")
            return {"status": "error", "output": "Script not found."}
            
        code_payload, language, script_name = row
        
        # Write to temporary sandbox file
        ext = ".py" if language == 'python' else ".js"
        temp_file = os.path.join(self.sandbox_dir, f"{script_hash}{ext}")
        with open(temp_file, "w", encoding="utf-8") as f:
            f.write(code_payload)
            
        logger.info(f"Executing '{script_name}' in Sandbox...")
        
        start_time = time.time()
        try:
            # Circuit Breaker: timeout enforces hard stop
            if language == 'python':
                cmd = [r"C:\Users\viper\python\python.exe", temp_file]
            else:
                cmd = ["node", temp_file]
                
            process = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout_seconds)
            
            # Step 48: Create success/failure feedback loop
            success = process.returncode == 0
            self._update_script_stats(script_hash, success)
            
            return {
                "status": "success" if success else "failed",
                "stdout": process.stdout,
                "stderr": process.stderr,
                "execution_time": time.time() - start_time
            }
            
        except subprocess.TimeoutExpired:
            logger.warning(f"CIRCUIT BREAKER: Script '{script_name}' exceeded {timeout_seconds}s timeout. Terminated.")
            self._update_script_stats(script_hash, False)
            return {"status": "timeout", "output": "Execution took too long and was terminated.", "execution_time": timeout_seconds}
        finally:
            if os.path.exists(temp_file):
                os.remove(temp_file)

    def _update_script_stats(self, script_hash: str, success: bool):
        timestamp = time.time()
        with self.get_db_connection() as conn:
            cursor = conn.cursor()
            # Moving average for success rate
            cursor.execute('SELECT success_rate, execution_count FROM scripts WHERE script_hash = ?', (script_hash,))
            row = cursor.fetchone()
            if row:
                old_rate, count = row
                new_count = count + 1
                new_rate = ((old_rate * count) + (1.0 if success else 0.0)) / new_count
                
                cursor.execute('''
                    UPDATE scripts 
                    SET success_rate = ?, execution_count = ?, last_executed = ?
                    WHERE script_hash = ?
                ''', (new_rate, new_count, timestamp, script_hash))
            conn.commit()

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    pyramid = ScriptPyramid()
    
    # Test valid script
    valid_code = "print('Pyramid Matrix Stable.')"
    hash_valid = pyramid.submit_script("sys_check", valid_code)
    res_valid = pyramid.execute_in_sandbox(hash_valid)
    print(f"Valid Result: {res_valid['stdout'].strip()}")
    
    # Test Infinite Loop (Circuit Breaker)
    evil_code = "while True:\n    pass"
    hash_evil = pyramid.submit_script("infinite_loop_test", evil_code)
    res_evil = pyramid.execute_in_sandbox(hash_evil, timeout_seconds=2)
    print(f"Evil Result Status: {res_evil['status']}")
