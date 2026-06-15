# [TIMESTAMP: 2026-06-08T09:30:00.000Z] [PROJECT_ID: SimsMerged-v1.4.2] [AGENT_ID: viper_cli-architectssj4]

import os
import json
import time
from typing import Dict
from .config import SSD_SANDBOX_PATH

METRICS_FILE = os.path.join(SSD_SANDBOX_PATH, "neural_metrics.json")

class MetricsCollector:
    """
    SCIENTIFIC METRICS COLLECTOR (PHASE 20):
    - Tracks real-time performance of each local model.
    - Records Success/Failure, Latency, and Logic Accuracy.
    - Feeds the Scientific Selector in the Neural Factory.
    """
    def __init__(self):
        self.stats = self._load()

    def _load(self):
        if os.path.exists(METRICS_FILE):
            with open(METRICS_FILE, "r") as f:
                return json.load(f)
        return {
            "models": {
                "qwen2.5:0.5b": {"success": 0, "fail": 0, "total_latency": 0.0, "logic_pass": 0},
                "smollm:135m": {"success": 0, "fail": 0, "total_latency": 0.0, "logic_pass": 0},
                "danube:latest": {"success": 0, "fail": 0, "total_latency": 0.0, "logic_pass": 0},
                "triton:latest": {"success": 0, "fail": 0, "total_latency": 0.0, "logic_pass": 0}
            }
        }

    def _save(self):
        with open(METRICS_FILE, "w") as f:
            json.dump(self.stats, f, indent=2)

    def report_inference(self, model, latency, success):
        if model not in self.stats["models"]:
            self.stats["models"][model] = {"success": 0, "fail": 0, "total_latency": 0.0, "logic_pass": 0}
        
        m = self.stats["models"][model]
        if success:
            m["success"] += 1
        else:
            m["fail"] += 1
        m["total_latency"] += latency
        self._save()

    def report_logic_pass(self, model):
        if model in self.stats["models"]:
            self.stats["models"][model]["logic_pass"] += 1
            self._save()

    def get_scientific_metrics(self) -> Dict:
        """Returns the sorted rankings for coding and logic."""
        rankings = {}
        for name, m in self.stats["models"].items():
            total = m["success"] + m["fail"]
            if total == 0:
                rankings[name] = {"coding": 0.5, "logic": 0.5}
                continue
                
            success_rate = m["success"] / total
            avg_latency = m["total_latency"] / total
            logic_score = m["logic_pass"] / max(1, m["success"])
            
            # Weighted Ranking
            coding_rank = (success_rate * 0.7) + (1.0 / max(1, avg_latency) * 0.3)
            rankings[name] = {
                "coding_score": round(coding_rank, 2),
                "logic_score": round(logic_score, 2),
                "reliability": round(success_rate, 2)
            }
        return rankings

metrics_collector = MetricsCollector()
