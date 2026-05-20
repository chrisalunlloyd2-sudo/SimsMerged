import time
import random

class QuantumCore:
    def __init__(self):
        self.system_tick = 0
        self.stability = 1.0
        self.heat = 35.0
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

    def cycle(self):
        self.system_tick += 1
        # Use defaults if keys missing
        lr = self.attributes.get('lr', 0.001)
        temp = self.attributes.get('temp', 0.7)
        
        lr_impact = (lr / 0.001) * 0.01
        temp_impact = (temp / 0.7) * 0.02
        
        self.stability -= (lr_impact + temp_impact) * random.uniform(0, 0.1)
        self.heat += (lr_impact * 10) + (temp_impact * 5)
        
        if self.stability < 0.5:
            self.stability += 0.005 # Slow self-healing
            
        self.stability = max(0.1, min(1.0, self.stability))
        self.heat = max(30.0, min(100.0, self.heat))
        
        return {
            'tick': self.system_tick,
            'stability': self.stability,
            'heat': self.heat,
            'active_attrs': self.attributes
        }
