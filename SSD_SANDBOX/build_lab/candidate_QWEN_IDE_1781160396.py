```python
class StabilityDecay:
    def __init__(self, core_node_distance):
        self.core_node_distance = core_node_distance

    def decay(self, distance_from_core):
        return 0.8 if (distance_from_core > self.core_node_distance) else 1 - 0.8 * (distance_from_core - self.core_node_distance)

class LogicEngineExtension:
    def __init__(self, grid_size, core_node_distance, decay_function=StabilityDecay