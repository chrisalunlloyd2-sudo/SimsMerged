```python
def calculate_stability_distance(grid, core_nodes):
    """
    Calculate stability distance based on grid and core nodes.

    Parameters:
    grid (list of list): The 2D grid representing the simulation environment.
    core_nodes (tuple): A tuple containing the coordinates of core nodes.

    Returns:
    float: Stability distance from each node to its closest core node.
    """
    distances = []
    for i in range(len(grid)):
        stable_core_node = None