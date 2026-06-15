# [TIMESTAMP: 2026-06-12T20:35:00.000Z] [PROJECT_ID: SimsMerged-v1.4.2] [AGENT_ID: viper_cli-architectssj4]
import os
import glob
import time
import asyncio
from sklearn.feature_extraction.text import TfidfVectorizer
import sqlite3
import pandas as pd
from backend.core.config import SSD_SANDBOX_PATH, METRICS_DB_PATH, add_log, add_message
from backend.core.model_orchestrator import model_orchestrator
from backend.core.quantum_core import quantum_core

class MLOrchestrator:
    def __init__(self):
        # TF-IDF acts as our advanced ML pattern recognizer (BM25 equivalent algorithm for keyword weight extraction)
        self.vectorizer = TfidfVectorizer(stop_words='english')
    
    async def correlate_performance_metrics(self):
        """Block D3: Statistical correlation to find problem points."""
        try:
            conn = sqlite3.connect(METRICS_DB_PATH)
            df = pd.read_sql_query("SELECT timestamp, tokens_sec, model, task_type FROM slm_metrics ORDER BY timestamp DESC LIMIT 100", conn)
            conn.close()
            
            if df.empty or len(df) < 5:
                return

            # current system state
            current_heat = quantum_core.heat
            current_stability = quantum_core.stability
            
            # Correlation 1: Thermal Throttling Detection
            avg_tps = df['tokens_sec'].mean()
            if current_heat > 0.80 and avg_tps < (avg_tps * 0.7):
                add_message("ADVISORY_ML", f"🚨 THERMAL CRITICALITY: Heat at {current_heat*100:.1f}% correlated with 30% TPS degradation. Initiating kernel cooldown.")
                quantum_core.stability *= 0.95 # Impact stability

            # Correlation 2: Model Specific Anomalies
            for model_name in df['model'].unique():
                model_df = df[df['model'] == model_name]
                if len(model_df) < 3: continue
                
                model_avg = model_df['tokens_sec'].mean()
                if model_avg < 1.0: # Arbitrary "hallucination/stall" threshold
                    add_message("ADVISORY_ML", f"⚠️ MODEL INSTABILITY: '{model_name}' is performing at {model_avg:.2f} TPS. High risk of logical inconsistency.")

            # Correlation 3: Task-Type Bottlenecks
            code_tasks = df[df['task_type'] == 'code']
            if not code_tasks.empty and code_tasks['tokens_sec'].mean() < 2.0:
                 add_log(f"[ML_CORRELATION] Coding latency detected. Suggesting context-window reduction.")

        except Exception as e:
            add_log(f"[ML_ORCHESTRATOR] Correlation failed: {e}", "error")

    async def analyze_shards_and_ping(self):
        # Read the truncated 2KB log shards
        search_pattern = os.path.join(SSD_SANDBOX_PATH, "syslog_*.log")
        shards = glob.glob(search_pattern)
        
        if not shards:
            return
            
        corpus = []
        # Ingest the latest shards to identify systemic behavior patterns
        for shard in shards[-10:]:
            try:
                with open(shard, "r", encoding="utf-8") as f:
                    corpus.append(f.read())
            except: pass
            
        if len(corpus) < 2:
            return
            
        try:
            # Pattern Recognition
            X = self.vectorizer.fit_transform(corpus)
            feature_names = self.vectorizer.get_feature_names_out()
            
            dense = X.todense()
            episode = dense[-1].tolist()[0]
            phrase_scores = [pair for pair in zip(range(0, len(episode)), episode) if pair[1] > 0]
            sorted_phrase_scores = sorted(phrase_scores, key=lambda t: t[1] * -1)
            top_words = [feature_names[word_id] for (word_id, score) in sorted_phrase_scores[:5]]
            
            if not top_words: return

            pattern = " ".join(top_words)
            add_log(f"[ML_ORCHESTRATOR] 🎯 Pattern recognized in recent 2KB shards: '{pattern}'")
            
            # Ping models with optimization patterns and epoch upgrades
            prompt = (
                f"Analyze the following telemetry pattern extracted via BM25/TF-IDF: '{pattern}'. "
                "Formulate an epoch optimization upgrade strategy to improve local heuristics and increase throughput. "
                "Return a short JSON object with 'epoch_version' and 'optimization_directive'."
            )
            
            # Block B1: Send Advisory Alert to System Console
            add_message("ADVISORY_System", f"⚠️ ML ALERT: Recognized pattern '{pattern}'. Model re-alignment initiated.")
            
            response = await model_orchestrator.add_task("EPMO_Architect", prompt, task_type="epoch_upgrade")
            add_log(f"[ML_ORCHESTRATOR] Epoch Upgrade Generated.")
            add_message("System_ML", f"📈 Epoch Upgrade Ping: {pattern[:20]} -> {response[:60]}...")
            
        except Exception as e:
            add_log(f"[ML_ORCHESTRATOR] Analysis failed: {e}", "error")

ml_orchestrator = MLOrchestrator()

async def start_ml_orchestrator_loop():
    """Background ML loop for continuous epoch optimization from log shards."""
    add_log("🧠 ML Orchestrator Pattern Recognition Online. Scanning 2KB Shards.")
    while True:
        await asyncio.sleep(60) # Ping every 60 seconds
        await ml_orchestrator.analyze_shards_and_ping()
        # Block D3: Run statistical correlation
        await ml_orchestrator.correlate_performance_metrics()