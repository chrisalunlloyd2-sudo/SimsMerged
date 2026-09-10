```python
import math

class StabilityDecay:
    def __init__(self, core_node_x, core_node_y):
        self.core_node_x = core_node_x
        self.core_node_y = core_node_y

    def decay_stability(self, x, y):
        distance_squared = (x - self.core_node_x) ** 2 + (y - self.core_node_y) ** 2
        stability_factor = 1.0 / math.sqrt(distance_squared)