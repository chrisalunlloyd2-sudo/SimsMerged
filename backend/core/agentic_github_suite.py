# [TIMESTAMP: 2026-06-12T21:15:00.000Z] [PROJECT_ID: SimsMerged-v1.4.2] [AGENT_ID: viper_cli-architectssj4]

import os
import time
import asyncio
from git import Repo
from backend.core.config import PROJECT_ROOT, add_log, add_message
from backend.core.model_orchestrator import model_orchestrator
from backend.core.data_syphon_epmo import epmo_school

class AgenticGitHubSuite:
    def __init__(self):
        self.repo_path = PROJECT_ROOT
        try:
            self.repo = Repo(self.repo_path)
            self.active = True
        except Exception as e:
            add_log(f"[GITHUB_SUITE] Initialization failed. Not a git repository: {e}", "error")
            self.active = False

    async def autonomous_sync_loop(self):
        if not self.active: return
        add_log("[GITHUB_SUITE] Agentic GitHub Governor Online. Monitoring codebase differentials.")

        while True:
            await asyncio.sleep(3600) # Check every hour
            try:
                await self.evaluate_and_commit()
            except Exception as e:
                add_log(f"[GITHUB_SUITE] Loop error: {e}", "error")

    async def evaluate_and_commit(self):
        if self.repo.is_dirty(untracked_files=True):
            add_log("[GITHUB_SUITE] Uncommitted changes detected. Initiating SLM analysis.")
            diff_text = self.repo.git.diff(None)
            untracked = self.repo.untracked_files

            # Block C1: Read recent log for context
            recent_log = ""
            try:
                recent_log = self.repo.git.log("-n 5", "--pretty=format:%s")
            except: pass

            # SLM Commit Generation
            prompt = (
                f"Recent Commit History:\n{recent_log}\n\n"
                f"Analyze the following git diff and untracked files: {untracked}. "
                f"Diff excerpt: {diff_text[:1500]}... "
                "Generate an enterprise-grade, conventional commit message detailing the "
                "novel research, component upgrades, and LSS scoring impacts. "
                "Follow the style of previous commits. Return ONLY the commit message."
            )

            commit_msg = await model_orchestrator.add_task("EPMO_Architect", prompt, task_type="github_sync")
            if not commit_msg or len(commit_msg) < 10:
                commit_msg = f"chore(auto): Autonomous component upgrade via ML Orchestrator."

            commit_msg = f"[TIMESTAMP: {time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime())}] {commit_msg}"

            # Execute Commit
            self.repo.git.add(all=True)
            self.repo.index.commit(commit_msg)
            add_log(f"[GITHUB_SUITE] Successfully committed: {commit_msg[:50]}...")
            add_message("System_Git", f"🧬 Branch advanced. Commit: {commit_msg[:50]}...")

            # Optional: push to remote if configured
            # origin = self.repo.remote(name='origin')
            # origin.push()

    async def create_optimization_branch(self, feature_name: str):
        """Creates a dedicated branch for Darwinian SLM testing."""
        if not self.active: return None
        branch_name = f"opt/{feature_name}_{int(time.time())}"
        try:
            # Ensure we are starting from main or the active baseline
            # self.repo.git.checkout('main')
            new_branch = self.repo.create_head(branch_name)
            new_branch.checkout()
            add_log(f"[GITHUB_SUITE] Checked out new optimization branch: {branch_name}")
            return branch_name
        except Exception as e:
            add_log(f"[GITHUB_SUITE] Failed to create branch: {e}", "error")
            return None

    async def darwinian_optimization_workflow(self, feature_name: str, target_file: str, improved_code: str):
        """
        Block C2 Mandate: Full Darwinian Branch Workflow.
        1. Create opt branch.
        2. Apply improved code.
        3. Run LSS Critique.
        4. Merge if score improves.
        """
        if not self.active: return False

        current_branch = self.repo.active_branch.name
        base_score = 0.0

        # 1. Measure Baseline
        try:
            with open(target_file, "r", encoding="utf-8") as f:
                current_code = f.read()
            base_score = epmo_school.critique_model_output(f"Optimize {target_file}", current_code)
        except: pass

        # 2. Spin up Opt Branch
        opt_branch = await self.create_optimization_branch(feature_name)
        if not opt_branch: return False

        try:
            # 3. Apply improvement
            with open(target_file, "w", encoding="utf-8") as f:
                f.write(improved_code)

            # 4. Measure New Score
            new_score = epmo_school.critique_model_output(f"Optimize {target_file}", improved_code)

            if new_score > base_score:
                add_log(f"[GITHUB_SUITE] Optimization success ({base_score:.2f} -> {new_score:.2f}). Initiating auto-merge.")
                # Commit on opt branch
                self.repo.git.add(target_file)
                self.repo.index.commit(f"opt: Improved LSS score for {target_file} to {new_score:.2f}")

                # Merge back
                self.repo.git.checkout(current_branch)
                self.repo.git.merge(opt_branch)
                add_message("System_Git", f"🚀 AUTO-MERGE: {feature_name} optimized to {new_score:.2f} LSS.")
                return True
            else:
                add_log(f"[GITHUB_SUITE] Optimization failed to beat baseline. Reverting branch.")
                self.repo.git.checkout(current_branch)
                # Cleanup branch
                self.repo.delete_head(opt_branch, force=True)
                return False

        except Exception as e:
            add_log(f"[GITHUB_SUITE] Darwinian workflow error: {e}", "error")
            self.repo.git.checkout(current_branch)
            return False

github_governor = AgenticGitHubSuite()

async def start_github_governor_loop():
    await github_governor.autonomous_sync_loop()
