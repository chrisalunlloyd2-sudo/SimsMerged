```python
import numpy as np

class StabilityDecay:
    def __init__(self, grid):
        self.grid = grid
        self.core_nodes = set(grid.keys())
        
    def simulate(self, time_steps=100):
        for step in range(time_steps):
            new_grid = {}
            for node in self.grid:
                distance_from_core = np.linalg.norm(node - self.core_nodes)
                if distance_from_core > 0.001:  # Adjust