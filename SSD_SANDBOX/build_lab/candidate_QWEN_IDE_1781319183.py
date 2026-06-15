```python
import numpy as np

def stability_decay(distance_from_core, core_nodes):
    """
    Calculate the decay factor based on the distance from core nodes.
    
    Parameters:
    - distance_from_core: A float representing the distance of a node from the core node.
    - core_nodes: An array containing the indices of all core nodes.

    Returns:
    - decay_factor: The calculated stability decay factor.
    """
    # Calculate the distance between each core node and every other core