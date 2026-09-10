```python
from collections import deque

def shortest_path(graph, start, end):
    """
    Finds the shortest path from 'start' to 'end' in the given graph represented as an adjacency list.

    Args:
        graph (dict): An adjacency list representing the graph.
        start: The starting node.
        end: The ending node.

    Returns:
        list: A list of edges forming the shortest path, or an empty list if no such path exists.
    """
    #