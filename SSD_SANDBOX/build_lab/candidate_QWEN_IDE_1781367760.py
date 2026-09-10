```python
import numpy as np

def calculate_stability_decay(grid):
    """
    Calculate and decay the stability based on distance from core nodes.

    Parameters:
    grid (list of lists): The simulation grid represented as a 2D list where 'core' represents
                          the core nodes and 'stability' represents the distance to other nodes.

    Returns:
    float: The updated stability values.
    """
    # Get the size of the grid
    rows, cols = len