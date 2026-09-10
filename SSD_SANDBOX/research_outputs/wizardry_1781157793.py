```python
import heapq

def find_shortest_path(start, end):
    """
    This function takes two parameters:
    start - a tuple representing the starting point (x1, y1)
    end - a tuple representing the destination point (x2, y2)

    It returns the shortest path between the start and end points
    as a list of integers [dx, dy], where dx is the change in x,
    and dy is the change in y.
    """