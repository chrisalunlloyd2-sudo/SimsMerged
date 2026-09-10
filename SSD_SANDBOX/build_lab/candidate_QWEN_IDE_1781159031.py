```python
import numpy as np

class StabilizationDecay:
    def __init__(self):
        self.decay_factor = 0.1  # Decay factor for stability decay

    def update_simulation_grid(self, simulation_grid):
        """
        Update the simulation grid based on distance from core nodes.
        :param simulation_grid: A list of tuples representing the positions in the grid
                                where each element is a tuple (x, y) with both coordinates relative to the origin