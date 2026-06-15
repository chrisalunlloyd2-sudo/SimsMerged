# [TIMESTAMP: 2026-06-08T07:40:00.000Z] [PROJECT_ID: SimsMerged-v1.4.2] [AGENT_ID: viper_cli-architectssj4]

import os
import time
import asyncio
import json
import random
from .config import SSD_SANDBOX_PATH, add_log, add_message

# THE BUILD LAB: A high-security, fenced directory for candidate code.
BUILD_LAB_DIR = os.path.join(SSD_SANDBOX_PATH, "build_lab")
os.makedirs(BUILD_LAB_DIR, exist_ok=True)

class QwenIDEWrapper:
    """
    QWEN-IDE WRAPPER (PHASE 15-17):
    - A specialized coding agent that operates at a 'Slow-Burn' pace.
    - Generates 'Candidate' code for game engine parts.
    - Implements a multi-stage safety verification and WISDOM TREE learning.
    """
    def __init__(self):
        self.active_tasks = []
        self.model_tag = "qwen2.5:0.5b" # Optimized for IDE-style instructions
        self.socrates_tag = "danube:latest" # Logic Verifier

    async def propose_coding_task(self, component_name, requirement):
        """Step 1: Initiation - Define what we want to build."""
        task_id = f"QWEN_IDE_{int(time.time())}"
        task = {
            "id": task_id,
            "component": component_name,
            "requirement": requirement,
            "status": "DRAFTING",
            "candidate_code": "",
            "verification_logs": [],
            "timestamp": time.time()
        }
        self.active_tasks.append(task)
        add_log(f"[QWEN_IDE] New coding task initiated: {task_id} ({component_name})")
        return task_id

    async def run_slow_burn_cycle(self):
        """The main autonomous loop for the Qwen-IDE."""
        from .model_orchestrator import model_orchestrator
        from .execution_engine import execution_sandbox
        from .wisdom_tree import wisdom_tree

        efficiency_mult = wisdom_tree.get_efficiency_mult()

        for task in self.active_tasks:
            if task["status"] == "DRAFTING":
                # Check for existing wisdom first (Never do same code 2 times)
                existing = wisdom_tree.get_wisdom(task["component"])
                if existing:
                    add_message("Qwen_IDE", f"📖 [WISDOM_REUSE] Found existing pattern for '{task['component']}'. Bypassing draft phase.")
                    task["candidate_code"] = existing["code"]
                    task["status"] = "VERIFYING"
                    continue

                # Step 2: Drafting - Scale wait time by efficiency multiplier
                base_wait = random.randint(60, 120)
                scaled_wait = base_wait * efficiency_mult
                add_message("Qwen_IDE", f"🧠 [DRAFTING] Thinking about '{task['component']}'... (Wait: {scaled_wait:.1f}s, mult: {efficiency_mult:.2f}x)")
                await asyncio.sleep(scaled_wait) 
                
                # Use Steer Points (Similar code) for context
                similar_patterns = wisdom_tree.search_wisdom(task["component"].split())
                steer_context = ""
                if similar_patterns:
                    steer_context = "REFERENCE WISDOM: " + json.dumps([p["code"][:100] for p in similar_patterns[:2]])

                prompt = (
                    f"You are the QWEN-IDE (Local-Only). TASK: Implement a game engine component: {task['component']}. "
                    f"REQUIREMENT: {task['requirement']}. {steer_context} "
                    "MANDATE: Output functional Python or JavaScript code. Output ONLY the code. "
                    "NEVER repeat verbatim existing wisdom; improve upon it or specialize it."
                )
                
                try:
                    code = await model_orchestrator.add_task("sprite_geek", prompt, task_type="qwen_ide_draft")
                    task["candidate_code"] = code
                    task["status"] = "VERIFYING"
                    
                    filename = f"candidate_{task['id']}.py"
                    task["filename"] = filename
                    filepath = os.path.join(BUILD_LAB_DIR, filename)
                    with open(filepath, "w", encoding="utf-8") as f:
                        f.write(code)
                    
                    add_log(f"[QWEN_IDE] Candidate generated: {filename}")
                except Exception as e:
                    add_log(f"[QWEN_IDE_ERR] Drafting failed for {task['id']}: {e}", "error")

            elif task["status"] == "VERIFYING":
                add_message("Judge_Socrates", f"⚖️ [REVIEWING] Auditing candidate code for '{task['component']}'...")
                await asyncio.sleep(random.randint(30, 60))
                
                # 1. Structural Preflight (JavaFX Specific)
                if "JavaFX" in task["component"] or "GUI" in task["component"]:
                    from .javafx_preflight import javafx_preflight
                    passed, msg = javafx_preflight.validate_code(task["candidate_code"])
                    if not passed:
                        add_message("Judge_Socrates", f"❌ [PREFLIGHT_FAIL] GUI structure error: {msg}")
                        task["status"] = "DRAFTING"
                        continue

                # 2. Logic Audit (Primary Model)
                verify_prompt = (
                    f"TECHNICAL AUDIT: Review the following candidate code for {task['component']}. "
                    f"CODE: {task['candidate_code']}. "
                    "Identify bugs, security flaws, or logic errors. "
                    "If safe, end with: STATUS: VERIFIED. Otherwise, provide a CRITIQUE."
                )
                
                try:
                    audit_res = await model_orchestrator.add_task("sprite_socrates", verify_prompt, task_type="qwen_ide_audit")
                    task["verification_logs"].append(audit_res)
                    
                    if "STATUS: VERIFIED" in audit_res.upper():
                        task["status"] = "SECURITY_CHECK"
                        add_message("System", f"✅ [CODE_VERIFIED] '{task['component']}' passed audit. Initiating Security Fence check.")
                    else:
                        add_message("Judge_Socrates", f"❌ [AUDIT_FAIL] {task['component']} needs refactoring: {audit_res[:200]}...")
                        task["status"] = "DRAFTING" 
                except: pass

            elif task["status"] == "SECURITY_CHECK":
                add_message("Security_Auditor", f"🛡️ [FENCING] Checking '{task['component']}' for RAM-bloat or network calls...")
                await asyncio.sleep(15)
                
                code = task["candidate_code"].lower()
                forbidden = ["requests.", "urllib.", "socket.", "import ram", "threading.", "multiprocessing."]
                violations = [p for p in forbidden if p in code]
                
                if not violations:
                    task["status"] = "STAGED"
                    add_message("System", f"💎 [STAGED] '{task['component']}' is ready for promotion. Use /api/promote/{task['id']} to integrate.")
                else:
                    add_message("Security_Auditor", f"⚠️ [SECURITY_VETO] Forbidden patterns found: {violations}. Redrafting...")
                    task["status"] = "DRAFTING"

    async def promote_to_production(self, task_id):
        """Step 5: Promotion - Move verified code to production and record wisdom."""
        task = next((t for t in self.active_tasks if t["id"] == task_id), None)
        if not task or task["status"] != "STAGED":
            return False, "Task not ready for promotion."

        from .wisdom_tree import wisdom_tree
        try:
            # Record in Wisdom Tree (LEARNING CYCLE)
            wisdom_tree.store_wisdom(task["component"], task["candidate_code"], {"task_id": task_id, "requirement": task["requirement"]})
            
            # Determine production path
            prod_dir = os.path.join(SSD_SANDBOX_PATH, "production_modules")
            os.makedirs(prod_dir, exist_ok=True)
            
            prod_filename = f"prod_{task['component'].lower().replace(' ', '_')}.py"
            src_path = os.path.join(BUILD_LAB_DIR, task["filename"])
            dest_path = os.path.join(prod_dir, prod_filename)
            
            # Atomic Move
            import shutil
            shutil.copy2(src_path, dest_path)
            
            task["status"] = "PROMOTED"
            add_message("System", f"🚀 [PROMOTED] '{task['component']}' is now live. Wisdom recorded. Tree expanded. 🌳")
            return True, f"Successfully promoted and learned {prod_filename}"
        except Exception as e:
            return False, str(e)

    def get_staged_tasks(self):
        return [t for t in self.active_tasks if t["status"] == "COMPLETED"]

qwen_ide = QwenIDEWrapper()

async def start_qwen_ide_loop():
    """Slow-Burn Loop: 1 task at a time, very slowly."""
    while True:
        # Check every 15-30 minutes (Much much slower)
        await asyncio.sleep(random.randint(900, 1800))
        try:
            await qwen_ide.propose_coding_task("Logic Engine Extension", "Add a 'stability' decay to the simulation grid based on distance from core nodes.")
            await qwen_ide.run_slow_burn_cycle()
        except: pass
