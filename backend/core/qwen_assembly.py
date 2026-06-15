# [TIMESTAMP: 2026-06-08T08:15:00.000Z] [PROJECT_ID: SimsMerged-v1.4.2] [AGENT_ID: viper_cli-architectssj4]

import os
import time
import asyncio
import random
import psutil
from .config import SSD_SANDBOX_PATH, add_log, add_message
from .model_orchestrator import model_orchestrator
from .execution_engine import execution_sandbox
from .wisdom_tree import wisdom_tree
from .evolution_council import evolution_council

ASSEMBLY_DIR = os.path.join(SSD_SANDBOX_PATH, "assembly_line")
os.makedirs(ASSEMBLY_DIR, exist_ok=True)

class QwenAssemblyLine:
    """
    PHASE 18: THE CIRCLE OF AGENTS
    A non-stop, CPU-aware coding assembly line passing performatives.
    Uses 'sprite_geek' (Qwen), 'sprite_writer' (Smollm), and 'sprite_socrates' (Danube).
    """
    def __init__(self):
        self.queue = []
        self.active_project = None
        self.idle_target = 99.0 # Only active when CPU is under 99%
        
    def add_project(self, name, objective):
        self.queue.append({
            "name": name,
            "objective": objective,
            "phase": "CRAWL",
            "context": "",
            "code": "",
            "attempts": 0
        })
        add_log(f"🏭 [ASSEMBLY_QUEUE] Added: {name}")
        
    async def run_loop(self):
        while True:
            # 1. CPU Monitor: Only talk when system is idle (50% target)
            cpu = psutil.cpu_percent(interval=0.1)
            if cpu > 50.0:
                await asyncio.sleep(10) # Wait for system to become idle
                continue
                
            # 2. Project Selection
            if not self.active_project and self.queue:
                self.active_project = self.queue.pop(0)
                add_message("System", f"🏭 [ASSEMBLY_LINE] Starting new project: {self.active_project['name']}")
                
            if not self.active_project:
                # Idle banter about code (The "Circle of Agents")
                await self.idle_banter()
                await asyncio.sleep(2) # Fast, non-stop talking
                continue
                
            # 3. Execution Pipeline
            p = self.active_project
            try:
                if p["phase"] == "CRAWL":
                    # Simulated Webcrawl / Memory Check by Smollm
                    add_message("sprite_writer", f"🕷️ [CRAWLER] Searching Wisdom Tree and web for: {p['objective']}")
                    wisdom = wisdom_tree.search_wisdom(p['objective'].split())
                    if wisdom:
                        p["context"] = wisdom[0]["code"]
                        add_message("sprite_writer", f"✅ [MEMORY] Found existing wisdom. Passing to Coder.")
                    else:
                        # Fallback to simulated evolution crawl
                        p["context"] = f"Web reference: Build a generic script."
                        add_message("sprite_writer", f"🌐 [WEBCRAWL] No local memory. Gathered external context. Passing to Coder.")
                    p["phase"] = "CODE"
                    
                elif p["phase"] == "CODE":
                    # Coding by Qwen
                    add_message("sprite_geek", f"💻 [QWEN_CODER] Implementing {p['name']}... (Attempt {p['attempts']+1})")
                    prompt = (
                        f"OBJECTIVE: {p['objective']}. CONTEXT: {p['context']}. "
                        "Output ONLY valid Python code to achieve this. Be concise. Do not use Markdown blocks."
                    )
                    code = await model_orchestrator.add_task("sprite_geek", prompt, task_type="assembly_code")
                    
                    # Clean up markdown if model hallucinated it
                    code = code.replace("```python", "").replace("```", "").strip()
                    p["code"] = code
                    
                    filename = f"{p['name'].replace(' ', '_').lower()}.py"
                    filepath = os.path.join(ASSEMBLY_DIR, filename)
                    with open(filepath, "w", encoding="utf-8") as f:
                        f.write(code)
                        
                    p["filename"] = filename
                    p["phase"] = "TEST"
                    
                elif p["phase"] == "TEST":
                    # Logic Gate by Socrates
                    add_message("Judge_Socrates", f"🧪 [LOGIC_GATE] Running execution test on {p['filename']}...")
                    result = execution_sandbox.run_script(p['filename'])
                    
                    if "SUCCESS" in result:
                        add_message("Judge_Socrates", f"🟩 [LOGIC_GATE: PASS] Code executed successfully! Output: {result[9:60]}...")
                        wisdom_tree.store_wisdom(p["name"], p["code"])
                        self.active_project = None # Done!
                    else:
                        p["attempts"] += 1
                        add_message("Judge_Socrates", f"🟥 [LOGIC_GATE: FAIL] Error: {result[:100]}...")
                        if p["attempts"] > 3:
                            add_message("System", f"☠️ [ASSEMBLY_ABORT] Project {p['name']} failed 3 times. Dropping.")
                            self.active_project = None
                        else:
                            p["context"] = f"PREVIOUS CODE:\n{p['code']}\nERROR:\n{result}\nFix this error."
                            p["phase"] = "CODE" # Pass back to coder
            except Exception as e:
                add_log(f"[ASSEMBLY_ERR] {e}", "error")
                self.active_project = None
                        
            await asyncio.sleep(1) # Fast loop when idle
            
    async def idle_banter(self):
        """Non-stop talking about code."""
        agents = ["sprite_geek", "sprite_writer", "sprite_newton"]
        topics = ["refactoring the AST parser", "optimizing SQLite I/O", "creating a new HUD widget", "implementing an API endpoint", "handling socket disconnects"]
        
        agent = random.choice(agents)
        topic = random.choice(topics)
        prompt = f"You are {agent} on a local SSD. The system is idle. Briefly discuss how we could go about {topic} in 1 sentence. Be highly technical."
        try:
            reply = await model_orchestrator.add_task(agent, prompt, task_type="idle_banter")
            add_message(agent, f"🗣️ [IDLE_BANTER] {reply}")
        except: pass

qwen_assembly = QwenAssemblyLine()

async def start_assembly_loop():
    await qwen_assembly.run_loop()
