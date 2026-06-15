```python
import numpy as np

class LogicEngine:
    def __init__(self, core_positions):
        self.core_positions = core_positions  # List of core nodes' positions in the grid
        self.stability_decay_factor = 0.1  # Decay factor for stability based on distance from core nodes

    def update_stability(self):
        """
        Update the stability values based on the decay factor.
        """
        new_stability_values = np.zeros(len(self.core_positions))