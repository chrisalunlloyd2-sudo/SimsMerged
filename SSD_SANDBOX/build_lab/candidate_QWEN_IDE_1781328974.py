```python
def stability_decay(distance_from_core):
    """
    A logic extension that simulates a grid based on a decay factor due to distance from core nodes.
    
    Parameters:
    - distance_from_core: The distance of the node from the core node (integer).
    
    Returns:
    - A function that takes 'distance_from_core' as input and returns the modified distance with stability decay.
    """
    def simulate_grid():
        # Simple example where each cell is randomly initialized