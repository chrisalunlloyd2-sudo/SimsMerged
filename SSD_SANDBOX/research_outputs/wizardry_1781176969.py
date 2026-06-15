```python
def city_pathfinder(start, end):
    """
    Finds the shortest distance between two cities in a grid.

    Args:
        start (int): The current starting point in the city.
        end (int): The ending point in the city.

    Returns:
        int: The distance to the destination city.
    """
    # Calculate the minimum distance from the start and end points
    dist = sum(abs((x - start) for x in range(start