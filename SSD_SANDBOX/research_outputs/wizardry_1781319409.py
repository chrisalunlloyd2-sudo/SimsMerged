Here's a possible implementation of the "city-pathfinding" task using Pyhton's built-in optimization algorithms:

```python
import timeit # for timing the algorithm
from collections import defaultdict

def path_cost(start, end):
    distance = {}  # create a dictionary to keep track of distances
    visited = set()   # create a set to check if we've been here already
    
    def dfs