```python
import numpy as np

def stability_decay(distance_grid, core_node):
    """
    Function to calculate the decay of stability based on distance from a core node.
    
    Parameters:
    - distance_grid: A 2D list representing the distance grid (e.g., distance between nodes).
    - core_node: The x-coordinate of the core node in the distance grid.
    
    Returns:
    - stability_decay: A float value representing the decay factor for the simulation grid.