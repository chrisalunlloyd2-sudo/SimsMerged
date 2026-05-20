import time
import random

class QuantumCore:
    def __init__(self):
        self.system_tick = 0
        self.stability = 1.0
        self.heat = 35.0
        self.cpu_frequency = 5.2 # Max GHz
        # 16-Core Affinity Matrix (0-15)
        self.core_load = {i: 0.0 for i in range(16)}
        
        # Memory & Swap States (User Selected Step 26)
        self.ram_load = 0.4 # 40% Baseline
        self.cas_latency = 32 # CL32
        self.is_swapping = False
        
        # Active AI Research Attributes
        self.attributes = {
            'lr': 0.001,
            'temp': 0.7,
            'dropout': 0.2,
            'ctx': 32768,
            'dim': 4096
        }

    def update_attributes(self, new_attrs):
        for k, v in new_attrs.items():
            if k in self.attributes:
                try:
                    self.attributes[k] = float(v)
                except:
                    self.attributes[k] = v

    def update_core_assignment(self, agent_list):
        """
        Calculates localized load for all 16 cores based on agent affinity.
        """
        # Reset core load
        for i in range(16): self.core_load[i] = 0.0
        
        # Also update RAM load based on agent count
        self.ram_load = min(1.0, len(agent_list) * 0.05 + 0.3)
        self.is_swapping = self.ram_load > 0.9
        
        for agent in agent_list:
            core = agent.get('cpu_core', 0)
            if 0 <= core <= 15:
                self.core_load[core] += 1.0

    def cycle(self):
        self.system_tick += 1
        lr = self.attributes.get('lr', 0.001)
        temp = self.attributes.get('temp', 0.7)
        
        # Base impacts
        lr_impact = (lr / 0.001) * 0.01
        temp_impact = (temp / 0.7) * 0.02
        
        # CORE CONGESTION IMPACT
        congestion_penalty = 0.0
        for core_id, load in self.core_load.items():
            if load > 1.0:
                congestion_penalty += (load - 1.0) * 0.05
        
        # ECC MEMORY CORRECTION
        base_penalty = (lr_impact + temp_impact + congestion_penalty) * random.uniform(0, 0.1)
        mitigated_penalty = base_penalty * 0.5 
        
        self.stability -= mitigated_penalty
        self.heat += (lr_impact * 10) + (temp_impact * 5) + (congestion_penalty * 20)
        
        # SWAP SLOWDOWN
        swap_penalty = 0.5 if self.is_swapping else 1.0
        
        # THERMAL THROTTLING LOGIC
        if self.heat > 80.0:
            reduction_factor = min(1.0, (self.heat - 80.0) / 20.0)
            self.cpu_frequency = (5.2 - (reduction_factor * (5.2 - 2.4))) * swap_penalty
        else:
            self.cpu_frequency = 5.2 * swap_penalty
            
        if self.stability < 0.5:
            self.stability += 0.005 # Slow self-healing
            
        self.stability = max(0.1, min(1.0, self.stability))
        self.heat = max(30.0, min(100.0, self.heat))
        
        return {
            'tick': self.system_tick,
            'stability': self.stability,
            'heat': self.heat,
            'frequency': self.cpu_frequency,
            'ram_load': self.ram_load,
            'is_swapping': self.is_swapping,
            'cas_latency': self.cas_latency,
            'core_load': self.core_load,
            'active_attrs': self.attributes
        }
