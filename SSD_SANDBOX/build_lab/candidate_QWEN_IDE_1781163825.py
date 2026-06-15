```python
import numpy as np

class StabilityDecay:
    def __init__(self, core_nodes):
        self.core_nodes = core_nodes
        self.decay_rate = 0.5
        self.time_to_decay = 10  # Time in seconds to decay the stability

    def simulate(self, grid_size, time_steps=100):
        """
        Simulates a simulation over a specified number of steps.
        
        Parameters:
        - grid_size: The