import os

base_path = r"C:\Users\viper\Desktop\SimsMerged"
core_path = os.path.join(base_path, "backend", "core", "quantum_core.py")

new_code = """
import time
import random

class QuantumCore:
    def __init__(self):
        self.system_tick = 0
        self.stability = 1.0
        self.heat = 35.0
        # Active AI Research Attributes (Defaults)
        self.attributes = {
            "lr": 0.001,
            "temp": 0.7,
            "dropout": 0.2,
            "ctx": 32768,
            "dim": 4096
        }

    def update_attributes(self, new_attrs):
        \"\"\"
        Updates the core attributes from the research node.
        \"\"\"
        for k, v in new_attrs.items():
            if k in self.attributes:
                self.attributes[k] = float(v) if isinstance(v, (int, float)) else v

    def cycle(self):
        \"\"\"
        Simulates a high-frequency system tick.
        Performance is now affected by research attributes.
        \"\"\"
        self.system_tick += 1

        # Logic: High Learning Rate or Temp increases instability and heat
        lr_impact = (self.attributes['lr'] / 0.001) * 0.01
        temp_impact = (self.attributes['temp'] / 0.7) * 0.02

        self.stability -= (lr_impact + temp_impact) * random.uniform(0, 0.1)
        self.heat += (lr_impact * 10) + (temp_impact * 5)

        # Self-healing logic
        if self.stability < 0.5:
            self.stability += 0.005 # Slow recovery

        self.stability = max(0.1, min(1.0, self.stability))
        self.heat = max(30.0, min(100.0, self.heat))

        return {
            "tick": self.system_tick,
            "stability": self.stability,
            "heat": self.heat,
            "active_attrs": self.attributes
        }
"""

with open(core_path, "w", encoding="utf-8") as f:
    f.write(new_code)

print("Quantum Core upgraded with functional research attribute logic!")
