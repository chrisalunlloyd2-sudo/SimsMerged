import os
import re

class ProgressionEngine:
    def __init__(self):
        self.global_level = 1
        self.total_xp = 0
        self.xp_to_next_level = 500
        self.unlocked_features = []
        self.agent_levels = {}
        self.system_buffs = {
            "packet_speed": 1.0,
            "stability_recovery": 1.0,
            "mint_yield": 1.0,
            "render_efficiency": 1.0
        }
        
        self.roadmap_tasks = self.load_roadmap()
        self.current_task_idx = 0
        
    def load_roadmap(self):
        tasks = []
        # Relative to backend/core/progression.py -> docs is up two levels then into docs
        roadmap_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "docs", "MASTER_ROADMAP.md"))
        if os.path.exists(roadmap_path):
            with open(roadmap_path, "r", encoding="utf-8") as f:
                pattern = re.compile(r"- \[([ xX])\] \*\*(Task|Feature) (\d+):\*\* (.+)")
                for line in f:
                    match = pattern.search(line)
                    if match:
                        tasks.append(f"Task {match.group(3)}: {match.group(4).strip()}")
        if not tasks:
            tasks = [f"Phase {i}: Procedural Evolution Step {i}" for i in range(1, 2201)]
        return tasks

    def add_agent_xp(self, agent_name, amount):
        if agent_name not in self.agent_levels:
            self.agent_levels[agent_name] = {"level": 1, "xp": 0, "title": "Novice Node"}
            
        agent = self.agent_levels[agent_name]
        agent["xp"] += amount
        self.total_xp += amount
        
        leveled_up_city = False
        
        # Agent Level Up
        if agent["xp"] >= agent["level"] * 100:
            agent["level"] += 1
            agent["xp"] = 0
            agent["title"] = self.get_agent_title(agent["level"])
            
        # Global City Level Up -> Unlock next roadmap feature
        if self.total_xp >= self.xp_to_next_level:
            self.global_level += 1
            self.total_xp -= self.xp_to_next_level
            self.xp_to_next_level = int(self.xp_to_next_level * 1.15) # Scaled growth
            self.unlock_next_feature()
            leveled_up_city = True
            
        return leveled_up_city
        
    def get_agent_title(self, level):
        titles = ["Novice Node", "Adept Router", "Expert Kernel", "Master Architect", "Ascendant Sentience", "Quantum Being"]
        return titles[min(level // 3, len(titles) - 1)]
        
    def unlock_next_feature(self):
        if self.current_task_idx < len(self.roadmap_tasks):
            feature = self.roadmap_tasks[self.current_task_idx]
            self.unlocked_features.append(feature)
            self.current_task_idx += 1
            if len(self.unlocked_features) > 10:
                self.unlocked_features.pop(0)
            self.apply_feature_logic(feature)

    def apply_feature_logic(self, feature_desc):
        """
        Translates procedural roadmap descriptions into real-world system changes.
        """
        f_lower = feature_desc.lower()
        if "packet" in f_lower or "bus" in f_lower:
            self.system_buffs["packet_speed"] += 0.002
        if "thread" in f_lower or "parallel" in f_lower:
            self.system_buffs["stability_recovery"] += 0.0002
        if "crypto" in f_lower or "mint" in f_lower:
            self.system_buffs["mint_yield"] += 0.1
        if "render" in f_lower or "visual" in f_lower:
            self.system_buffs["render_efficiency"] += 0.02

    def get_state(self):
        return {
            "level": self.global_level,
            "total_xp": self.total_xp,
            "next_level_xp": self.xp_to_next_level,
            "recent_unlocks": self.unlocked_features,
            "agent_stats": self.agent_levels,
            "progress_pct": round((self.total_xp / self.xp_to_next_level) * 100, 2),
            "buffs": self.system_buffs
        }
