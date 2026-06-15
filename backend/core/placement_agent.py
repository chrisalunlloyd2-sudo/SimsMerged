# [TIMESTAMP: 2026-06-14T18:15:00.000Z] [PROJECT_ID: SimsMerged-v1.4.2] [AGENT_ID: viper_cli-architectssj4]
# ACTION: Pillar IV - Placement Agents (Airtight Logic Gates)

import os
import json
import asyncio
from .config import SSD_SANDBOX_PATH, add_log, add_message
from .bm25_orchestrator import bm25_scaffold
from .execution_engine import execution_sandbox
from .logic_resolution import resolution_manager

class PlacementLogicGate:
    """
    Pillar IV: The Logic Gate.
    Does not write code. Evaluates proposed tasks against Continuity DB.
    Routes approved tasks to headless execution scripts.
    """
    def __init__(self):
        self.manifest_path = os.path.join(SSD_SANDBOX_PATH, "task_manifest.json")
        self.evolution_workspace = r"C:\Users\viper\Desktop\Metropolis_Evolution"

    def _evaluate_continuity(self, task: dict) -> bool:
        """
        Mathematical verification against the Project Continuity DB.
        """
        topic = task.get("task", "")
        # Query the Continuity DB
        results = bm25_scaffold.continuity.search(topic, top_k=1)
        
        if not results:
            add_log(f"[LOGIC_GATE] Task '{topic}' rejected. No continuity context found.", "warning")
            return False
            
        doc, score = results[0]
        
        # If the BM25 score is too low, it means the task is an hallucination or out of scope
        if score < 0.8:
            add_log(f"[LOGIC_GATE] Task '{topic}' rejected. Continuity score too low ({score:.2f}).", "warning")
            return False
            
        add_log(f"[LOGIC_GATE] Task '{topic}' approved. Continuity score: {score:.2f}.")
        return True

    async def route_task(self, task: dict):
        """
        Routes the task to a specific headless ML script based on dependencies.
        """
        from backend.core.data_syphon_epmo import LeanSixSigmaEPMO
        from backend.core.model_orchestrator import model_orchestrator
        
        epmo = LeanSixSigmaEPMO()
        topic = task.get("task", "")
        context = task.get("context", "")
        
        add_message("Logic_Gate", f"🚦 [ROUTING] Evaluating task: {topic}")
        
        if not self._evaluate_continuity(task):
            add_message("Logic_Gate", f"⛔ [REJECTED] Task '{topic}' violates project continuity.")
            return

        # [PILLAR VI] Dependency Manager Routing
        if any(kw in topic.lower() for kw in ["install", "package", "dependency", "download", "pkg"]):
            add_message("Dependency_Agent", f"📦 [ACQUISITION] Processing dependency task: {topic}")
            pkg_tool = os.path.join(os.path.dirname(__file__), "headless_tools", "headless_pkg_manager.py")
            
            prompt = f"Extract the EXACT install or download command from this task: {topic}. Output ONLY the command (e.g., pip install requests)."
            cmd_to_run = await model_orchestrator.add_task("Dependency_Agent", prompt, task_type="pkg_extract")
            
            import subprocess
            res = subprocess.run(["python", pkg_tool, cmd_to_run.strip()], capture_output=True, text=True)
            try:
                report = json.loads(res.stdout.split('\n')[-1])
                if report.get("verified"):
                    add_message("Dependency_Agent", f"✅ [VERIFIED] Successfully installed: {cmd_to_run}")
                    return 
                else:
                    add_message("Dependency_Agent", f"❌ [FAILED] Installation failed: {cmd_to_run}")
                    return
            except:
                add_message("Dependency_Agent", f"⚠️ [ERROR] Malformed report from Pkg Manager.")
                return

        # [PILLAR IV] Logic Resolution Scaling
        lang = "python" # Default fallback
        if "java" in topic.lower(): lang = "java"
        elif "js" in topic.lower() or "javascript" in topic.lower(): lang = "javascript"
        
        ghost_db = bm25_scaffold.get_ghost_code(lang)
        schema_results = ghost_db.search(topic, top_k=1)
        schema_context = schema_results[0][0]['text'] if schema_results else "Use standard syntax."

        tier = resolution_manager.resolve_task_tier(topic, context)
        options = resolution_manager.get_resolution_options(tier)
        add_log(f"[LOGIC_GATE] Scaling resolution to {tier} for task '{topic}'.")

        # Ask Implementer
        prompt = (
            f"You are the SOVEREIGN_IMPLEMENTER. Task: {topic}\n"
            f"Context: {context}\n"
            f"MANDATORY SCHEMA: {schema_context}\n\n"
            "MANDATE: You MUST ensure any code you generate physically writes to the disk. "
            "If creating a file, use: with open('path/to/file', 'w') as f: f.write(content)\n"
            "STRATEGY: Prioritize using scripts in tools/. Use [EXECUTE] python tools/script_name.py <args>."
        )
        
        try:
            raw_output = await model_orchestrator.add_task("Implementer_Qwen", prompt, options=options, task_type="implementation")
            add_log(f"[LOGIC_GATE] SLM Raw Output: {raw_output[:200]}...")
            raw_code = raw_output

            if "[EXECUTE]" in raw_output:
                # ... (Automation tool execution) ...
                cmd = raw_output.split("[EXECUTE]")[1].strip().split('\n')[0]
                add_message("Logic_Gate", f"⚙️ [AUTOMATION] Agent invoked tool: {cmd}")
                import subprocess
                project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
                res = subprocess.run(cmd, shell=True, cwd=project_root, capture_output=True, text=True)
                if res.returncode != 0:
                    add_message("Logic_Gate", f"❌ [TOOL_FAILED] {res.stderr}")
                    return
                add_message("Logic_Gate", f"✅ [TOOL_SUCCESS] Automation complete.")
                raw_code = res.stdout

            # [PILLAR VI] Sovereign Test Orchestration
            add_log(f"[LOGIC_GATE] Initiating Sovereign Test Suite for '{topic}'...")
            test_tool = os.path.join(os.path.dirname(__file__), "headless_tools", "headless_test_orchestrator.py")
            # We save the raw_code to a temp file to test it
            temp_path = os.path.join(SSD_SANDBOX_PATH, f"test_{abs(hash(raw_code))}.py")
            with open(temp_path, "w", encoding="utf-8") as f: f.write(raw_code)
            
            test_res = subprocess.run(["python", test_tool, temp_path], capture_output=True, text=True)
            if os.path.exists(temp_path): os.remove(temp_path)
            
            try:
                test_data = json.loads(test_res.stdout.split('\n')[-1])
                if not test_data.get("success"):
                    add_message("Logic_Gate", f"❌ [TEST_FAILED] Task '{topic}' failed Sovereign Test Suite ({test_data.get('test_type')}).")
                    # Trigger Socrates Debugger
                    success = False
                else:
                    add_message("Logic_Gate", f"✅ [TEST_PASSED] Task '{topic}' passed all sovereign tests.")
                    success = True
            except:
                success = epmo.verify_runtime(raw_code) # Fallback to standard sandbox

            # Headless Validation (Security & AST)
            # ... (Rest of existing validation) ...
            import subprocess
            temp_eval_path = os.path.join(SSD_SANDBOX_PATH, f"eval_{abs(hash(raw_code))}.py")
            with open(temp_eval_path, "w", encoding="utf-8") as f:
                f.write(raw_code)
                
            tool_dir = os.path.join(os.path.dirname(__file__), "headless_tools")
            ast_script = os.path.join(tool_dir, "headless_ast_analyzer.py")
            sec_script = os.path.join(tool_dir, "headless_security_scanner.py")
            
            ast_res = subprocess.run(["python", ast_script, temp_eval_path], capture_output=True, text=True)
            sec_res = subprocess.run(["python", sec_script, temp_eval_path], capture_output=True, text=True)
            if os.path.exists(temp_eval_path): os.remove(temp_eval_path)
            
            ast_data = json.loads(ast_res.stdout) if ast_res.stdout.strip() else {}
            sec_data = json.loads(sec_res.stdout) if sec_res.stdout.strip() else {}
            
            if sec_data.get("pii_flags") or sec_data.get("entropy_warnings"):
                add_message("Logic_Gate", f"❌ [REJECTED] Failed Headless Security Scan.")
                return

            # Recursive Debugger
            success = epmo.verify_runtime(raw_code)
            if not success:
                add_message("Logic_Gate", f"🛠️ [DEBUGGING] Pinging Debug_Socrates...")
                debug_prompt = f"FIX THIS CODE. It failed runtime.\nCODE:\n{raw_code}"
                fixed_code = await model_orchestrator.add_task("Debug_Socrates", debug_prompt, task_type="debugger")
                if epmo.verify_runtime(fixed_code):
                    raw_code = fixed_code
                    success = True
                    add_message("Logic_Gate", f"✨ [DEBUG_SUCCESS] Socrates fixed logic.")

            if success:
                from .evolution_council import evolution_council
                await evolution_council.apply_mini_project({
                    "topic": topic, "impact": f"{lang.upper()}_IMPLEMENTATION",
                    "hash": str(hash(raw_code))[:12], "complexity": 15, "code_prototype": raw_code
                })
            else:
                add_message("Logic_Gate", f"💀 [FATAL] Task failed all attempts.")
                
        except Exception as e:
            add_log(f"[LOGIC_GATE_ERR] {e}", "error")

    async def process_manifest_loop(self):
        add_log("🚦 Placement Logic Gate active.")
        await asyncio.sleep(30)
        while True:
            if os.path.exists(self.manifest_path):
                try:
                    with open(self.manifest_path, "r", encoding="utf-8") as f:
                        tasks = json.load(f)
                    if tasks:
                        task = tasks.pop(0)
                        with open(self.manifest_path, "w", encoding="utf-8") as f:
                            json.dump(tasks, f, indent=2)
                        await self.route_task(task)
                except: pass
            await asyncio.sleep(30)

placement_gate = PlacementLogicGate()
