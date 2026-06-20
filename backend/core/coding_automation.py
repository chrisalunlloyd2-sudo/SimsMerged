# [TIMESTAMP: 2026-06-07T20:10:00.000Z] [PROJECT_ID: SimsMerged-v1.4.2] [AGENT_ID: Gemini-CLI-Architect]

import os
import ast
import yaml

os.environ["GIT_PYTHON_GIT_EXECUTABLE"] = r"C:\Users\viper\git\cmd\git.exe"
import git
import duckdb
from typing import List, Dict, Optional
from .config import SSD_SANDBOX_PATH

CODE_RETRIEVAL_PATH = os.path.join(SSD_SANDBOX_PATH, "external_code_cache")

class CodingAutomation:
    """
    NON-LLM CODING AUTOMATION:
    - Heuristic and AST-based code analysis and retrieval.
    - Uses 'Git Mirror' strategy to retrieve code without API quotas.
    - Integrates DuckDB for high-speed retrieval of local code patterns.
    """
    def __init__(self):
        db_path = os.path.join(SSD_SANDBOX_PATH, "automation_patterns.duckdb")
        try:
            self.db = duckdb.connect(db_path)
        except duckdb.IOException as e:
            print(f"[CODING_AUTOMATION] Failed to open persistent DB: {e}. Falling back to in-memory.")
            self.db = duckdb.connect(':memory:')
        self._init_db()

    def _init_db(self):
        self.db.execute('''
            CREATE TABLE IF NOT EXISTS code_patterns (
                pattern_id VARCHAR PRIMARY KEY,
                language VARCHAR,
                pattern_type VARCHAR, -- 'class', 'function', 'decorator'
                ast_fingerprint VARCHAR,
                raw_code TEXT,
                source_repo VARCHAR
            )
        ''')

    def retrieve_github_repo(self, repo_url: str):
        """Step 1: The 'Git Mirror' Method (No API Quota)."""
        repo_name = repo_url.split("/")[-1].replace(".git", "")
        target_path = os.path.join(CODE_RETRIEVAL_PATH, repo_name)

        if not os.path.exists(target_path):
            print(f"[AUTOMATION] Mirroring repo: {repo_url}")
            git.Repo.clone_from(repo_url, target_path, depth=1)
        return target_path

    def analyze_ast(self, file_path: str):
        """Step 2: Non-LLM AST Fingerprinting."""
        with open(file_path, "r", encoding="utf-8") as f:
            try:
                node = ast.parse(f.read())
                for item in node.body:
                    if isinstance(item, ast.ClassDef):
                        self._store_pattern(item.name, "python", "class", ast.dump(item), ast.unparse(item))
                    elif isinstance(item, ast.FunctionDef):
                        self._store_pattern(item.name, "python", "function", ast.dump(item), ast.unparse(item))
            except Exception:
                pass

    def _store_pattern(self, name, lang, p_type, fingerprint, code):
        self.db.execute('''
            INSERT OR IGNORE INTO code_patterns (pattern_id, language, pattern_type, ast_fingerprint, raw_code)
            VALUES (?, ?, ?, ?, ?)
        ''', (name, lang, p_type, fingerprint, code))

    def get_pattern(self, name: str) -> Optional[str]:
        res = self.db.execute('SELECT raw_code FROM code_patterns WHERE pattern_id = ?', (name,)).fetchone()
        return res[0] if res else None

coding_automation = CodingAutomation()
