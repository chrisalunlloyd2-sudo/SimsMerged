```python
import numpy as np

def stability_decay(distance_from_core_node):
    """
    Function to calculate the decay of stability based on distance from core nodes.
    
    Parameters:
    - distance_from_core_node: Distance from a core node in grid coordinates.

    Returns:
    - decayed_distance: The calculated decay of distance from core nodes.
    """
    # Convert distance from grid coordinates to 2D array
    distance_array = np.array([distance_from_core_node] * len