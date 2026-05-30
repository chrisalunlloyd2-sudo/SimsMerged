# TIMESTAMP: 2026-05-29T01:38:00.000Z
# PROJECT_ID: SimsMerged-v1.3-Metropolis
# AGENT_ID: Antigravity-Agent

import time
import random

class QuantumCore:
    def __init__(self):
        self.system_tick = 0
        self.stability = 1.0
        self.heat = 35.0
        self.cpu_frequency = 5.2 # Max GHz
        
        # RESOURCE FENCING (GEMINI Mandate)
        self.resource_fence_active = True
        self.cpu_throttle_limit = 0.70 # Hard limit to 70% to ensure host stability
        
        # 16-Core Affinity Matrix (0-15)
        self.core_load = {i: 0.0 for i in range(16)}
        
        # Memory & Swap States
        self.ram_load = 0.4
        self.cas_latency = 32
        self.is_swapping = False
        self.multi_channel_mode = True
        
        # Row Hammer States
        self.charge_leakage = 0.0
        self.row_hammer_protection = True
        
        # Memory Isolation
        self.isolation_enabled = True
        self.sandboxes = {}
        
        # Dirty Bit Page Marking
        self.dirty_pages = set()
        
        # Zero-Copy Mode
        self.zero_copy_active = True
        
        # Predictive Prefetching
        self.prefetch_enabled = True
        self.prefetch_hit_rate = 0.85
        
        # VRAM & Cold Storage
        self.vram_shadow_active = True
        self.cold_storage_pages = {} # (x, y): last_access_time
        self.iops_lag_remaining = 0
        
        # Speculation & Pressure
        self.speculative_execution_active = True
        self.branch_accuracy = 0.82
        self.memory_pressure_active = False
        
        # DRAM Refresh Cycle (User Selected Step 35 Option B)
        self.refresh_cycle_active = False
        self.refresh_timer = 0
        self.refresh_interval = 10000 # Increased interval to reduce performance hits
        self.refresh_duration = 3  # Reduced duration for less stalling
        
        # Active AI Research Attributes
        self.attributes = {
            'lr': 0.001,
            'temp': 0.7,
            'dropout': 0.2,
            'ctx': 32768,
            'dim': 4096
        }

    def update_attributes(self, attr_map):
        """
        [TIMESTAMP: 2026-05-25T03:21:00.452Z][PROJECT_ID: SimsMerged-v1.3][AGENT_ID: Antigravity-Agent]
        Updates the active AI attributes dictionary.
        """
        for k, v in attr_map.items():
            self.attributes[k] = v

    def process_agent_stability(self, agent_name, raw_stability):
        """
        Processes agent stability through a sandbox isolation layer.
        """
        if agent_name not in self.sandboxes:
            self.sandboxes[agent_name] = {"load_history": [], "isolation_score": 1.0}
        
        # Simple isolation logic: if stability is very low, sandbox it more
        isolation_score = 1.0
        if raw_stability < 0.5:
            isolation_score = 0.8 # 20% penalty for unstable agents
        
        self.sandboxes[agent_name]["isolation_score"] = isolation_score
        return raw_stability * isolation_score

    def update_core_assignment(self, agents):
        """
        Updates the 16-core affinity matrix based on active agents.
        """
        # Reset core loads
        for i in range(16):
            self.core_load[i] = 0.0
            
        if not agents:
            return

        for i, agent in enumerate(agents):
            core_id = i % 16
            # Map agent working set/stability to core load
            load = (1.0 - agent.get('stability', 1.0)) + (agent.get('working_set_kb', 0) / 102400.0)
            self.core_load[core_id] += load

    def trigger_hammer_event(self):
        """
        Simulates a Row Hammer attack by increasing charge leakage.
        Returns 'MITIGATED' if protection is on, else 'VULNERABLE'.
        """
        self.charge_leakage += 0.5
        if self.row_hammer_protection:
            return "MITIGATED"
        return "VULNERABLE"

    def flush_dirty_pages(self):
        """
        Clears the dirty pages set and returns the count of flushed pages.
        """
        count = len(self.dirty_pages)
        self.dirty_pages.clear()
        return count

    def update_access_time(self, x, y):
        """
        Updates the access time for a tile to prevent it from becoming 'Cold'.
        If the tile was already cold, it triggers an IOPS lag spike.
        """
        now = time.time()
        if (x, y) in self.cold_storage_pages:
            # Check if tile has faded to 'Cold' (e.g., 60 seconds of inactivity)
            if now - self.cold_storage_pages[(x, y)] > 60:
                self.iops_lag_remaining = 5 # 5 cycle lag spike
        self.cold_storage_pages[(x, y)] = now

    def mark_page_dirty(self, x, y):
        """
        Marks a specific grid coordinate as 'Dirty' (Modified).
        """
        self.dirty_pages.add((x, y))
        self.update_access_time(x, y)

    def cycle(self, env_nodes=None):
        self.system_tick += 1
        
        # ENVIRONMENTAL THERMAL DISSIPATION
        dissipation_rate = 0.5 # Base cooling
        if env_nodes:
            water_count = len([n for n in env_nodes if n.get('type') == 'WATER'])
            tree_count = len([n for n in env_nodes if n.get('type') == 'TREE'])
            # Each water node adds 2.0 cooling, trees add 0.5
            dissipation_rate += (water_count * 2.0) + (tree_count * 0.5)
        
        self.heat -= dissipation_rate
        
        # DRAM REFRESH CYCLE LOGIC (Step 35 Option B)
        self.refresh_timer += 1
        if not self.refresh_cycle_active:
            if self.refresh_timer >= self.refresh_interval:
                self.refresh_cycle_active = True
                self.refresh_timer = 0
        else:
            if self.refresh_timer >= self.refresh_duration:
                self.refresh_cycle_active = False
                self.refresh_timer = 0
        
        # IOPS LAG SPIKE
        effective_freq_mult = 1.0
        if self.iops_lag_remaining > 0:
            self.iops_lag_remaining -= 1
            effective_freq_mult = 0.1 
        
        # REFRESH STALL
        if self.refresh_cycle_active:
            effective_freq_mult = 0.0 # Total halt during refresh

        lr = self.attributes.get('lr', 0.001)
        temp = self.attributes.get('temp', 0.7)
        
        # 1. Row Hammer Leakage Dissipation
        if self.charge_leakage > 0:
            self.charge_leakage -= 0.01 
        self.charge_leakage = max(0, self.charge_leakage)
        
        # Base impacts
        lr_impact = (lr / 0.001) * 0.01
        temp_impact = (temp / 0.7) * 0.02
        
        # CORE CONGESTION IMPACT
        congestion_penalty = 0.0
        for core_id, load in self.core_load.items():
            if load > 1.0:
                congestion_penalty += (load - 1.0) * 0.05
        
        # ECC MEMORY CORRECTION
        base_penalty = (lr_impact + temp_impact + congestion_penalty + self.charge_leakage) * random.uniform(0, 0.1)
        mitigated_penalty = base_penalty * 0.5 
        
        self.stability -= mitigated_penalty
        self.heat += (lr_impact * 10) + (temp_impact * 5) + (congestion_penalty * 20) + (self.charge_leakage * 50)
        
        # SWAP SLOWDOWN
        swap_penalty = 0.5 if self.is_swapping else 1.0
        # MULTI-CHANNEL BOOST
        channel_boost = 1.25 if self.multi_channel_mode else 1.0
        
        # THERMAL THROTTLING LOGIC
        if self.heat > 80.0:
            reduction_factor = min(1.0, (self.heat - 80.0) / 20.0)
            self.cpu_frequency = (5.2 - (reduction_factor * (5.2 - 2.4))) * swap_penalty * channel_boost * effective_freq_mult
        else:
            self.cpu_frequency = 5.2 * swap_penalty * channel_boost * effective_freq_mult
            
        # RESOURCE FENCING: Hard Throttling to 25% if active
        if self.resource_fence_active:
            self.cpu_frequency = min(self.cpu_frequency, 5.2 * self.cpu_throttle_limit)
            
        if self.stability < 0.6:
            self.stability += 0.012 # Enhanced core self-healing under strict VIPER guidelines
            
        self.stability = max(0.1, min(1.0, self.stability))
        self.heat = max(30.0, min(100.0, self.heat))
        
        # Identify Cold Pages for Frontend
        now = time.time()
        cold_pages = [[x, y] for (x, y), t in self.cold_storage_pages.items() if now - t > 60]
        
        return {
            'tick': self.system_tick,
            'stability': self.stability,
            'heat': self.heat,
            'frequency': self.cpu_frequency,
            'ram_load': self.ram_load,
            'is_swapping': self.is_swapping,
            'is_refreshing': self.refresh_cycle_active,
            'leakage': self.charge_leakage,
            'cas_latency': self.cas_latency,
            'multi_channel': self.multi_channel_mode,
            'vram_shadow': self.vram_shadow_active,
            'cold_pages': cold_pages,
            'iops_lag': self.iops_lag_remaining > 0,
            'core_load': self.core_load,
            'active_attrs': self.attributes,
            'resource_fence_active': self.resource_fence_active,
            'row_hammer_protection': self.row_hammer_protection,
            'speculative_execution': self.speculative_execution_active,
            'prefetch_enabled': self.prefetch_enabled
        }
