```python
import numpy as np

class LogicEngineExtension:
    def __init__(self, simulation_grid):
        self.simulation_grid = simulation_grid
        self.stability_decay = 0.95  # Decay factor for stability

    def update_stability(self, distance_from_core):
        new_stability = (1 - self.stability_decay) * distance_from_core + \
                        self.stability_decay * np.max(np.abs(self.simulation_grid - self.simulation_grid.ne