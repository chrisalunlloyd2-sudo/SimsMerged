```python
import numpy as np

def calculate_stability_decay(distance_from_core):
    """
    Calculate and return a stability decay factor based on distance from core nodes.
    
    Parameters:
    - distance_from_core: A float representing the distance of each node in the simulation grid from the core nodes.
    
    Returns:
    - A float value indicating the stability decay factor for the given distance.
    """

    # Define the decay factor based on the provided distance
    if distance_from_core >