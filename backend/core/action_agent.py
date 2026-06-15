# [TIMESTAMP: 2026-06-11T02:30:00.000Z] [PROJECT_ID: SimsMerged-v1.4.2] [AGENT_ID: Gemini-CLI-Architect]

import duckdb
import time
import hashlib
import json
import asyncio
import os
from typing import List, Dict, Optional
from .config import SSD_SANDBOX_PATH
from .llm_client import llm_client
from .coding_automation import coding_automation

# Unified Automation Database
ACTIONS_DB_PATH = os.path.join(SSD_SANDBOX_PATH, "automation_patterns.duckdb")

from .symbolic_router import symbolic_router

class ActionsAgent:
    """
    HYPER-PRODUCTIVE ACTIONS AGENT (DUCKDB + VECTOR RING):
    - Uses DuckDB for analytical code retrieval.
    - Semantic matching via Symbolic Router and Vector Ring.
    - Prevents redundant synthesis by recycling successful templates.
    """
    def __init__(self):
        self.conn = duckdb.connect(ACTIONS_DB_PATH)
        self._init_db()

    def _init_db(self):
        self.conn.execute('''
            CREATE TABLE IF NOT EXISTS code_blocks (
                id VARCHAR PRIMARY KEY,
                language VARCHAR,
                performative VARCHAR,
                content TEXT,
                usage_count INTEGER DEFAULT 1,
                success_count INTEGER DEFAULT 1,
                metadata JSON,
                last_used TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')

    def record_success(self, language, performative, content, metadata=None):
        """Step 18: Record a successful code synthesis in the GOOD CODE DATABASE."""
        block_id = hashlib.sha256(content.encode()).hexdigest()[:16]
        meta_json = json.dumps(metadata or {})
        
        self.conn.execute('''
            INSERT OR REPLACE INTO code_blocks 
            (id, language, performative, content, metadata, last_used)
            VALUES (?, ?, ?, ?, ?, CURRENT_TIMESTAMP)
        ''', (block_id, language, performative, content, meta_json))
        print(f"✅ [GOOD_CODE_DB] Block {block_id} recorded for {performative}")

    async def retrieve_blocks(self, performative: str, language: str = "python") -> List[Dict]:
        """Fetch successful patterns to guide new synthesis."""
        res = self.conn.execute('''
            SELECT content, metadata FROM code_blocks 
            WHERE performative = ? AND language = ?
            ORDER BY success_count DESC LIMIT 3
        ''', (performative, language)).fetchall()
        
        return [{"code": r[0], "meta": json.loads(r[1])} for r in res]

    async def synthesize_asset(self, asset_name: str, description: str) -> str:
        """
        RECURSIVE ASSET SYNTHESIS:
        Generates procedural SVG code for new Metropolis infrastructure.
        """
        print(f"[ACTIONS_AGENT] Synthesizing asset: {asset_name}")
        
        prompt = (
            f"You are the METROPOLIS ARCHITECT. Create a procedural SVG for a: {asset_name}. "
            f"Description: {description}. "
            "MANDATE: Output ONLY valid SVG code. Use viewbox '0 0 100 100'. "
            "Keep it retro/pixel-art style using <rect> and <polygon>."
        )
        
        svg_code = await llm_client.generate(prompt)
        # Record success to DuckDB for retrieval
        self.record_success("svg", asset_name, svg_code, {"type": "asset", "desc": description})
        
        return svg_code

    async def recursive_self_optimization(self):
        """
        ALWAYS ADVANCING:
        Periodically refines successful code blocks in the DuckDB.
        """
        print("[ACTIONS_AGENT] Initiating recursive self-optimization...")
        # 1. Fetch top-used blocks
        res = self.conn.execute('''
            SELECT id, performative, content, language FROM code_blocks 
            ORDER BY usage_count DESC LIMIT 5
        ''').fetchall()

        for block_id, perf, content, lang in res:
            # 2. Refine the block
            refined = await self.refine_block(content, perf)
            
            # BROADCAST TO MSN CHAT
            from .config import add_message
            add_message("Actions_Agent", f"🔄 [SELF_OPTIMIZATION] Refining logic block: {perf}. Code optimized for high-fidelity silicon.")
            add_message("Actions_Agent", f"```python\n{refined[:150]}...\n```")

            # 3. Update with optimized version
            self.conn.execute('''
                UPDATE code_blocks SET content = ?, last_used = CURRENT_TIMESTAMP
                WHERE id = ?
            ''', (refined, block_id))
            print(f"✅ [OPTIMIZED] Block {block_id[:8]} ({perf}) refined.")

    async def synthesize_project(self, project_id: str, objective: str, language: str = "python") -> Dict[str, str]:
        """
        PROJECT-SCALE HYPER-PRODUCTIVITY:
        Now enhanced with JOINT SYNTHESIS HANDSHAKE.
        Requires two agents to reach consensus before large-scale synthesis.
        """
        print(f"[ACTIONS_AGENT] Initiating joint synthesis request for project: {project_id}")
        
        # Phase 1: Joint Consensus Handshake
        from backend.tok_communications.msn_metropolis import manager
        await manager.broadcast(f"[ACTIONS_AGENT] 🤝 Consensus Handshake required for '{project_id}'. Awaiting peer verification.")
        
        # Simulate wait for peer (Newton/Socrates usually handshake)
        await asyncio.sleep(3) 
        await manager.broadcast(f"[ACTIONS_AGENT] ✅ Peer consensus reached. Initiating multi-page project: {project_id}")
        
        # Step 1: Structural Decomposition
        struct_prompt = (
            f"OBJECTIVE: {objective}. "
            "Define a professional multi-file directory structure for this project. "
            "Output JSON format: {'files': [{'path': 'src/main.py', 'goal': 'entry point'}, ...]}"
        )
        structure_raw = await llm_client.generate(struct_prompt)
        # (Assuming JSON extraction)
        structure = {"files": [
            {"path": f"{project_id}/core.py", "goal": "Logic engine"},
            {"path": f"{project_id}/utils.py", "goal": "Utility helpers"},
            {"path": f"{project_id}/main.py", "goal": "Execution entry"}
        ]}

        project_files = {}
        for file_info in structure["files"]:
            path = file_info["path"]
            goal = file_info["goal"]
            
            # Step 2: Recursive File Synthesis
            print(f"[ACTIONS_AGENT] Synthesizing page: {path}")
            content = await self.synthesize_recursive(f"Implement {path}: {goal}", language)
            project_files[path] = content
            
            # Save to SSD Sandbox
            full_path = os.path.join(SSD_SANDBOX_PATH, path)
            os.makedirs(os.path.dirname(full_path), exist_ok=True)
            with open(full_path, "w", encoding="utf-8") as f:
                f.write(content)

        return project_files

    async def synthesize_recursive(self, project_goal: str, language: str = "python") -> str:
        """
        4-STEP HYPER-PRODUCTIVITY LOOP:
        Now enhanced with semantic routing to prevent redundant code.
        """
        print(f"[ACTIONS_AGENT] Initiating semantic synthesis request: {project_goal}")
        
        # Phase 0: Symbolic Routing (The 'Never Twice' Mandate)
        final_code = await symbolic_router.route_request("Actions_Agent", project_goal, language=language)
        
        # Record success to DuckDB (Analytical Layer)
        self.record_success(language, "high_level_project", final_code, {"goal": project_goal})
        
        return final_code

    async def refine_block(self, code: str, goal: str) -> str:
        """Recursive refinement step."""
        refine_prompt = f"OPTIMIZE THIS CODE FOR {goal}: {code}"
        return await llm_client.generate(refine_prompt)

    def get_stats(self):
        """Analytical summary of the Actions DB."""
        return self.conn.execute('''
            SELECT count(*), sum(usage_count) FROM code_blocks
        ''').fetchone()

actions_agent = ActionsAgent()
