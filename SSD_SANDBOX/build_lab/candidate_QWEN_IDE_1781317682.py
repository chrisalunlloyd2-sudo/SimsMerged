```python
class StabilityDecayEngine:
    def __init__(self, core_grid):
        self.grid = core_grid

    def update(self, distance_from_core_node: float) -> None:
        """
        Update the stability decay based on the distance from the core nodes.

        Parameters:
        - distance_from_core_node (float): The distance in grid units from a core node.
        """
        for row, line in enumerate(self.grid):
            for col, element in enumerate(line):