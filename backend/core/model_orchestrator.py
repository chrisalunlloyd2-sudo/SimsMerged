# [TIMESTAMP: 2026-06-05T08:45:00.000Z] [PROJECT_ID: SimsMerged-v1.4] [AGENT_ID: Antigravity-CLI-Architect]

import asyncio
import json
import os
import time
import random
import urllib.request
from collections import deque
import sqlite3
from .config import METRICS_DB_PATH, SSD_SANDBOX_PATH, DISTRICTS, METROPOLIS_AGENTS

class ModelOrchestrator:
    def __init__(self):
        self.queue = deque()
        self.is_processing = False
        self.db_path = METRICS_DB_PATH
        self.console_log = os.path.join(SSD_SANDBOX_PATH, "neural_console.log")
        self.findings_log = os.path.join(SSD_SANDBOX_PATH, "swarm_findings.json")

        # ACTUAL LOCAL OLLAMA TAGS
        self.agent_model_map = {
            "sprite_geek": "qwen2.5:0.5b",
            "sprite_writer": "smollm:135m",
            "sprite_socrates": "danube:latest",
            "sprite_newton": "triton:latest",
            "journalist_prime": "smollm:135m",
            "comm_analyzer": "qwen2.5:0.5b"
        }

        self._init_metrics_db()
        self._init_findings_log()

        # CPU THROTTLE CONFIG (Slow-Burn Mandate)
        self.cpu_load_limit = 0.35 # Throttle if host CPU > 35%
        self.base_cooldown = 5.0 # High base cooldown for "Slow-Burn"
        self.speculative_enabled = True
        self.lstm_throughput_enabled = True

    def _init_metrics_db(self):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS slm_metrics (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp REAL,
                agent_id TEXT,
                model TEXT,
                tokens_sec REAL,
                total_latency REAL,
                context_size INTEGER,
                prediction_len INTEGER,
                task_type TEXT
            )
        ''')
        conn.commit()
        conn.close()

    def _init_findings_log(self):
        if not os.path.exists(self.findings_log):
            with open(self.findings_log, "w") as f:
                json.dump([], f)

    def _record_metrics(self, agent_id, model, tokens_sec, latency, ctx, pred_len, task_type):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO slm_metrics (timestamp, agent_id, model, tokens_sec, total_latency, context_size, prediction_len, task_type)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (time.time(), agent_id, model, tokens_sec, latency, ctx, pred_len, task_type))
        conn.commit()
        conn.close()

    def _log_console(self, agent_name, prompt, response):
        timestamp = time.ctime()
        entry = (
            f"\n--- [NEURAL_CONSOLE] {timestamp} ---\n"
            f"AGENT: {agent_name}\n"
            f"PROMPT_STUB: {prompt[:100]}...\n"
            f"RESPONSE: {response}\n"
            f"--------------------------------------\n"
        )
        try:
            with open(self.console_log, "a", encoding="utf-8") as f:
                f.write(entry)
        except: pass

    def record_finding(self, agent_id, finding, hypothesis):
        try:
            with open(self.findings_log, "r") as f:
                findings = json.load(f)
            findings.append({
                "timestamp": time.time(),
                "agent_id": agent_id,
                "finding": finding,
                "hypothesis": hypothesis
            })
            with open(self.findings_log, "w") as f:
                json.dump(findings[-50:], f, indent=2)
        except: pass

    def get_performance_stats(self):
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute('''
                SELECT model, AVG(tokens_sec), AVG(total_latency), COUNT(*)
                FROM slm_metrics
                GROUP BY model
            ''')
            rows = cursor.fetchall()
            conn.close()
            return [
                {"model": r[0], "avg_tps": round(r[1], 2), "avg_latency": round(r[2], 3), "samples": r[3]}
                for r in rows
            ]
        except: return []

    def set_agent_model(self, agent_id, model_tag):
        if agent_id in self.agent_model_map:
            self.agent_model_map[agent_id] = model_tag
            return True
        return False

    async def add_task(self, agent_id, prompt, options=None, task_type="chat"):
        future = asyncio.get_event_loop().create_future()
        self.queue.append({
            "agent_id": agent_id,
            "prompt": prompt,
            "options": options or {"num_ctx": 512, "num_predict": 100, "temperature": 0.7, "num_thread": 1},
            "future": future,
            "type": task_type
        })
        if not self.is_processing:
            asyncio.create_task(self._process_queue())
        return await future

    async def _process_queue(self):
        import psutil
        self.is_processing = True
        while self.queue:
            cpu_usage = psutil.cpu_percent(interval=None)
            if cpu_usage > (self.cpu_load_limit * 100):
                await asyncio.sleep(5.0 * (cpu_usage / 100.0))

            refractor_count = len([d for d in DISTRICTS if d.get("type") == "REFRACTOR"])
            dynamic_cooldown = max(1.0, self.base_cooldown * (0.8 ** refractor_count))

            task = self.queue.popleft()
            agent_id = task["agent_id"]

            agent = next((a for a in METROPOLIS_AGENTS if a["id"] == agent_id), None)
            if agent and "IO_BUFFER_OVERCLOCK" in agent.get("traits", []):
                dynamic_cooldown *= 0.5

            model = self.agent_model_map.get(agent_id, "qwen2.5:0.5b")

            try:
                start_time = time.perf_counter()

                # SPECULATIVE DECODING SCAFFOLD
                draft_text = ""
                if self.speculative_enabled and task["type"] == "code":
                    draft_model = "smollm:135m"
                    draft_prompt = f"### [DRAFT]\n{task['prompt']}\n### [CONTINUE CODE]"
                    draft_res = await self._call_ollama_raw(agent_id, draft_model, draft_prompt, {"num_predict": 50, "temperature": 0.2})
                    draft_text = draft_res.get('response', '').strip()

                # LSTM THROUGHPUT MULTIPLIER
                predictive_hint = ""
                if self.lstm_throughput_enabled and task["type"] == "code":
                    from .predictive_engine import predictive_engine
                    if predictive_engine.is_hydrated:
                        predictive_hint = predictive_engine.speak_code(task["prompt"][:100], length=30)

                final_prompt = task["prompt"]
                if draft_text or predictive_hint:
                    final_prompt = f"{task['prompt']}\n[DRAFT_HINT: {draft_text}]\n[LSTM_HINT: {predictive_hint}]\nVerify and complete:"

                full_res = await self._call_ollama_raw(agent_id, model, final_prompt, task["options"])
                response_text = full_res.get('response', '').strip()

                latency = time.perf_counter() - start_time

                # Block D2: Tokens Per Second Calculation
                eval_count = full_res.get('eval_count', 0)
                eval_duration = full_res.get('eval_duration', 1) # in nanoseconds
                tps = eval_count / (eval_duration / 1e9) if eval_duration > 0 else 0

                from backend.sprite_triplet.depin_wallet import DePINLedger
                depin_ledger = DePINLedger()
                depin_ledger.charge_inference_fee(agent_id, task["options"].get("num_ctx", 512))

                self._record_metrics(agent_id, model, tps, latency, task["options"].get("num_ctx", 0), eval_count, task["type"])
                agent_name = agent["name"] if agent else agent_id
                self._log_console(agent_name, final_prompt, response_text)
                task["future"].set_result(response_text)

            except Exception as e:
                if not task["future"].done(): task["future"].set_exception(e)

            await asyncio.sleep(dynamic_cooldown)
        self.is_processing = False

    async def _call_ollama_raw(self, agent_id, model, prompt, options):
        def _call():
            req = urllib.request.Request("http://localhost:11434/api/generate", headers={"Content-Type": "application/json"})
            data = json.dumps({
                "model": model,
                "prompt": prompt,
                "agent_id": agent_id,
                "stream": False,
                "options": options
            }).encode('utf-8')
            with urllib.request.urlopen(req, data=data, timeout=300.0) as response:
                return json.loads(response.read().decode('utf-8'))

        return await asyncio.to_thread(_call)

model_orchestrator = ModelOrchestrator()
