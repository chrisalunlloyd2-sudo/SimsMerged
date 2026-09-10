# [TIMESTAMP: 2026-06-14T18:45:00.000Z] [PROJECT_ID: SimsMerged-v1.4.2] [AGENT_ID: viper_cli-architectssj4]
# ACTION: Autonomous Agentic GitHub Sync & Data Hydration (Pillar III)

import os
import time
import asyncio
import subprocess
import re
import random
from .config import SSD_SANDBOX_PATH, add_log, add_message
from .bm25_orchestrator import bm25_scaffold
from .model_orchestrator import model_orchestrator
from .headless_tools.headless_auth_manager import auth_manager

class AgenticGitHubSync:
    """
    Pillar III: Replaces manual user backups with Sovereign Agent Commits.
    Includes data hydration and PII Scrubbing logic.
    """
    def __init__(self):
        self.project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
        self.sync_interval = 3600 * 4 # Sync every 4 hours

    async def _sync_gui_assets(self):
        """Pillar V: Native asset synchronization."""
        add_log("[GITHUB_SYNC] Synchronizing sovereign GUI assets...")
        script = os.path.join(os.path.dirname(__file__), "headless_tools", "headless_asset_sync.py")
        subprocess.run(["python", script], capture_output=True)

    def _scrub_pii(self, content: str) -> str:
        """Removes local paths, usernames, and potential secrets before ingestion/upload."""
        # Scrub standard Windows/Linux user paths
        content = re.sub(r'C:\\Users\\[\w\\]+', 'C:\\Users\\[REDACTED]\\', content, flags=re.IGNORECASE)
        content = re.sub(r'/home/\w+/', '/home/[REDACTED]/', content, flags=re.IGNORECASE)
        # Scrub obvious tokens/keys
        content = re.sub(r'(?i)(api_key|secret|token|password)[\s=:]+[\'"]?[\w\-]+[\'"]?', r'\1 = "[REDACTED]"', content)
        return content

    async def hydrate_databases(self):
        """
        Agents actively query the web/simulated environment to learn new coding schemas
        and hydrate their specific language databases.
        """
        add_log("[GITHUB_SYNC] Initiating autonomous data hydration crawl...")

        # Simulated Web/GitHub Crawl Targets
        targets = [
            {"topic": "Advanced JavaFX concurrency patterns", "lang": "java"},
            {"topic": "Python Neo4j integration and graph traversal", "lang": "python"},
            {"topic": "Secure OAuth2 implementations in FastAPI", "lang": "python"},
            {"topic": "ES6 isometric game engine rendering loops", "lang": "javascript"}
        ]

        target = random.choice(targets)

        prompt = (
            f"You are the Data Hydration Agent. Research and provide a highly advanced, "
            f"production-ready code schema for: {target['topic']}. "
            "Output ONLY the raw code block. No markdown, no explanations."
        )

        try:
            raw_code = await model_orchestrator.add_task("Hydration_Agent", prompt, task_type="data_crawl")
            scrubbed_code = self._scrub_pii(raw_code)

            ghost_db = bm25_scaffold.get_ghost_code(target['lang'])
            ghost_db.update_learning(
                scrubbed_code,
                metadata={
                    "topic": target['topic'],
                    "source": "autonomous_crawl",
                    "lss_weight": 1.2 # Baseline for unverified external code
                }
            )
            add_log(f"[HYDRATION] Successfully learned '{target['topic']}' and stored in {target['lang']} DB.")
        except Exception as e:
            add_log(f"[HYDRATION_ERR] Failed to hydrate data: {e}", "warning")

    async def execute_agentic_commit(self):
        """Autonomously stages, commits, and (simulates) push to GitHub."""
        add_log("[GITHUB_SYNC] Executing Sovereign Commit Sequence.")
        try:
            # 1. Sync assets first
            await self._sync_gui_assets()

            # 2. Generate commit message
            syslog_path = os.path.join(SSD_SANDBOX_PATH, "syslog.log")
            recent_logs = ""
            if os.path.exists(syslog_path):
                with open(syslog_path, "r", encoding="utf-8") as f:
                    lines = f.readlines()
                    recent_logs = "".join(lines[-20:])

            prompt = (
                f"You are the GitHub Governor. Based on these recent system logs, generate a concise, "
                f"professional git commit message. ONLY output the commit string.\n\nLOGS:\n{recent_logs}"
            )
            commit_msg = await model_orchestrator.add_task("GitHub_Governor", prompt, task_type="commit_gen")
            commit_msg = commit_msg.strip().replace('"', "'")
            if not commit_msg: commit_msg = "Autonomous Evolution Sync"

            # 3. Check for auth
            token = auth_manager.get_token()
            if not token or "[UNINITIALIZED]" in token:
                 add_log("[GITHUB_SYNC] Auth token uninitialized. Skipping remote push.", "warning")

            # 4. Git sequence
            subprocess.run(["git", "add", "."], cwd=self.project_root, check=False)
            subprocess.run(["git", "commit", "-m", f"[AGENTIC_SYNC] {commit_msg}"], cwd=self.project_root, check=False)

            add_message("GitHub_Governor", f"🌐 [SYNC_COMPLETE] Sovereign commit anchored. Message: '{commit_msg}'")

        except Exception as e:
            add_log(f"[GITHUB_SYNC_ERR] {e}", "error")

    async def run_sync_loop(self):
        add_log("🌐 Agentic GitHub Sync loop active.")
        # Pillar III: Initial data hydration
        from .hydrate_continuity import hydrate
        hydrate()

        await asyncio.sleep(60) # Initial delay
        while True:
            await self.hydrate_databases()
            await asyncio.sleep(120) # Hydrate frequently

            if random.random() > 0.5: # Periodic commits
                await self.execute_agentic_commit()

            await asyncio.sleep(self.sync_interval)

github_governor = AgenticGitHubSync()
