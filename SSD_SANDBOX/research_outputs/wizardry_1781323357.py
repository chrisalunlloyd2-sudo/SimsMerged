```python
def city_pathfinder(start, end):
    """Return the shortest distance between two cities."""
    if not isinstance(start, (int, float)) or not isinstance(end, (int, float)):
        raise ValueError("Both inputs must be of type int or float.")

    distances = [0] * (len(end) + 1)
    for i in range(2**len(set(range(min(i, end), min(start,