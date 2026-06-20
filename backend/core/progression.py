# TIMESTAMP: 2026-05-28T12:00:00.123Z
# PROJECT_ID: SimsMerged-v1.3
# AGENT_ID: Antigravity-Agent

import os
import re

class ProgressionEngine:
    def __init__(self):
        self.global_level = 1
        self.total_xp = 0
        self.xp_to_next_level = 500
        self.unlocked_features = []
        self.agent_levels = {}
        self.singularity_active = False
        self.SINGULARITY_THRESHOLD = 100

        # System Buffs & Genetic Multipliers (Step 45 Genetic civilization Upgrade)
        self.system_buffs = {
            "packet_speed": 1.0,
            "stability_recovery": 1.0,
            "mint_yield": 1.0,
            "render_efficiency": 1.0,
            "danube_accuracy_mult": 1.0, # Genetic upgrade that improves AI decisions
            "ecc_recovery_rate": 1.0,
            "singularity_power": 0.0
        }

        self.roadmap_tasks = self.load_roadmap()
        self.current_task_idx = 0

    def load_roadmap(self):
        tasks = []
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

    def evaluate_promotion(self, agent_name, level):
        """
        Determines the agent's vocational title based on their performance level.
        Now supports standard "Aider Danube" promotions.
        """
        if level >= 12:
            return "Quantum DePIN Oracle"
        elif level >= 8:
            return "Danube Systems Architect"
        elif level >= 5:
            return "Aider Senior Architect"
        elif level >= 3:
            return "Aider Junior Developer"
        return "Novice Aider Bot"

    def get_building_bonus(self, env_nodes):
        """
        Calculates active buffs based on the city's zoning/infrastructure.
        - BANKS -> Mint Yield
        - HOSPITALS -> Stability Recovery
        - SCHOOLS -> AI Accuracy
        - RESEARCH -> Packet Speed
        """
        bonuses = {
            "mint_yield": 0.0,
            "stability_recovery": 0.0,
            "danube_accuracy_mult": 0.0,
            "packet_speed": 0.0
        }
        if not env_nodes: return bonuses

        for node in env_nodes:
            ntype = node.get('type')
            if ntype == 'BANK': bonuses['mint_yield'] += 0.05
            elif ntype == 'HOSPITAL': bonuses['stability_recovery'] += 0.02
            elif ntype == 'SCHOOL': bonuses['danube_accuracy_mult'] += 0.03
            elif ntype == 'RESEARCH': bonuses['packet_speed'] += 0.01

        return bonuses

    def add_agent_xp(self, agent_name, amount):
        """
        Awards XP to agents and triggers global genetic updates upon level transitions.
        """
        if agent_name not in self.agent_levels:
            self.agent_levels[agent_name] = {"level": 1, "xp": 0, "title": "Novice Aider Bot", "name": agent_name}

        agent = self.agent_levels[agent_name]
        agent["xp"] += amount
        self.total_xp += amount

        leveled_up_city = False

        # Agent Level Up & Promotion
        if agent["xp"] >= agent["level"] * 100:
            agent["level"] += 1
            agent["xp"] = 0
            agent["title"] = self.evaluate_promotion(agent["name"], agent["level"])

        # Global City Level Up -> Triggers Genetic Upgrade!
        if self.total_xp >= self.xp_to_next_level:
            self.global_level += 1
            self.total_xp -= self.xp_to_next_level
            self.xp_to_next_level = int(self.xp_to_next_level * 1.15) # Scaled growth

            # Check for Singularity
            if self.global_level >= self.SINGULARITY_THRESHOLD and not self.singularity_active:
                self.singularity_active = True
                self.system_buffs["singularity_power"] = 1.0
                print("[SINGULARITY] Metropolis Core reached Level 100. Universal constants aligned.")

            # Trigger procedural upgrades
            self.unlock_next_feature()
            self.apply_genetic_upgrade()
            leveled_up_city = True

        return leveled_up_city

    def apply_genetic_upgrade(self):
        """
        Procedurally evolves system parameters upon civilization milestones.
        Mutates weights and improves environmental and AI decision bounds automatically.
        """
        # Multipliers mutate genetically based on the active level
        self.system_buffs["packet_speed"] *= 1.05
        self.system_buffs["stability_recovery"] *= 1.08
        self.system_buffs["mint_yield"] *= 1.03
        self.system_buffs["danube_accuracy_mult"] *= 1.05
        self.system_buffs["ecc_recovery_rate"] *= 1.06

    def get_agent_title(self, level):
        # Kept for backward compatibility
        return self.evaluate_promotion("", level)

    def unlock_next_feature(self):
        if self.current_task_idx < len(self.roadmap_tasks):
            feature = self.roadmap_tasks[self.current_task_idx]
            self.unlocked_features.append(feature)
            self.current_task_idx += 1
            if len(self.unlocked_features) > 10:
                self.unlocked_features.pop(0)
            self.apply_feature_logic(feature)

    def apply_feature_logic(self, feature_desc):
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
            "buffs": self.system_buffs,
            "singularity_active": self.singularity_active
        }
