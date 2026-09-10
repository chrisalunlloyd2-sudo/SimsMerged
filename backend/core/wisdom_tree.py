# [TIMESTAMP: 2026-06-08T07:25:00.000Z] [PROJECT_ID: SimsMerged-v1.4.2] [AGENT_ID: viper_cli-architectssj4]

import os
import json
import hashlib
import time
from typing import List, Dict, Optional
from .config import SSD_SANDBOX_PATH, add_log

WISDOM_DB_PATH = os.path.join(SSD_SANDBOX_PATH, "wisdom_tree.json")

class WisdomTree:
    """
    THE WISDOM TREE (PHASE 17):
    - Persistent repository of all verified code and technical logic.
    - Prevents duplicate synthesis.
    - Provides 'Steer Points' for the Qwen-IDE to reuse existing wisdom.
    """
    def __init__(self):
        self.tree = self._load_tree()

    def _load_tree(self) -> Dict:
        if os.path.exists(WISDOM_DB_PATH):
            with open(WISDOM_DB_PATH, "r", encoding="utf-8") as f:
                return json.load(f)
        return {
            "patterns": {}, # hash -> {code, component, timestamp}
            "steer_points": {}, # component_name -> [list of pattern hashes]
            "evolution_metrics": {"total_optimized_blocks": 0, "efficiency_multiplier": 1.0}
        }

    def _save_tree(self):
        with open(WISDOM_DB_PATH, "w", encoding="utf-8") as f:
            json.dump(self.tree, f, indent=2)

    def store_wisdom(self, component, code, metadata=None):
        """Stores a new verified pattern in the tree."""
        code_hash = hashlib.sha256(code.encode()).hexdigest()

        if code_hash in self.tree["patterns"]:
            return False, "Wisdom already exists."

        entry = {
            "component": component,
            "code": code,
            "hash": code_hash,
            "timestamp": time.time(),
            "metadata": metadata or {}
        }

        self.tree["patterns"][code_hash] = entry

        if component not in self.tree["steer_points"]:
            self.tree["steer_points"][component] = []
        self.tree["steer_points"][component].append(code_hash)

        self.tree["evolution_metrics"]["total_optimized_blocks"] += 1
        # GRADUAL SPEED-UP: Every 5 blocks, reduce the wait time by 5% (max 50% reduction)
        new_mult = max(0.5, 1.0 - (self.tree["evolution_metrics"]["total_optimized_blocks"] // 5) * 0.05)
        self.tree["evolution_metrics"]["efficiency_multiplier"] = new_mult

        self._save_tree()
        add_log(f"🌳 [WISDOM_GROWN] New logic for '{component}' added to the Tree. Efficiency: {new_mult:.2f}x")
        return True, code_hash

    def get_summary(self):
        """Returns a technical summary of the Wisdom Tree."""
        return {
            "total_blocks": self.tree["evolution_metrics"]["total_optimized_blocks"],
            "efficiency": self.tree["evolution_metrics"]["efficiency_multiplier"],
            "latest_components": [p["component"] for p in list(self.tree["patterns"].values())[-5:]]
        }

    def get_wisdom(self, component) -> Optional[Dict]:
        """Retrieves existing wisdom for a component to prevent duplicate work."""
        hashes = self.tree["steer_points"].get(component, [])
        if not hashes:
            return None
        # Return the most recent pattern
        return self.tree["patterns"][hashes[-1]]

    def search_wisdom(self, requirement_keywords: List[str]) -> List[Dict]:
        """Search for similar code patterns to guide new synthesis."""
        results = []
        for p in self.tree["patterns"].values():
            if any(kw.lower() in p["code"].lower() for kw in requirement_keywords):
                results.append(p)
        return results

    def get_efficiency_mult(self):
        return self.tree["evolution_metrics"].get("efficiency_multiplier", 1.0)

wisdom_tree = WisdomTree()
