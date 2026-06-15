```python
import numpy as np

class StabilizationDecay:
    def __init__(self, core_nodes):
        self.core_nodes = core_nodes
        self.stability_decay_rate = 0.5  # Decay rate of stability in percentage

    def simulate_simulation(self, simulation_grid):
        """
        Simulates the decay of the stability based on distance from core nodes.
        
        :param simulation_grid: 2D numpy array representing the current state of the grid