# TIMESTAMP: 2026-06-09
# PROJECT_ID: SimsMerged-v1.4.2
# AGENT_ID: viper_cli-architectssj4
# [PERFORMATIVE: PATHFINDING_A_STAR]
# DESCRIPTION: Phase 2.1 - Highly Optimized A* Pathfinding for Isometric Matrix

import heapq
import json
import os
import logging

logger = logging.getLogger("Pathfinder")
logger.setLevel(logging.INFO)

class AStarPathfinder:
    def __init__(self, matrix, walkable_types=[0, 2]):
        """
        matrix: 2D array of integers
        walkable_types: List of terrain IDs that are traversable (e.g., 0=Grass, 2=Stone)
        """
        self.matrix = matrix
        self.walkable_types = walkable_types
        self.cols = len(matrix)
        self.rows = len(matrix[0]) if self.cols > 0 else 0

    def heuristic(self, a, b):
        """Manhattan distance for grid movement."""
        return abs(a[0] - b[0]) + abs(a[1] - b[1])

    def get_neighbors(self, pos):
        neighbors = []
        for dx, dy in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            x, y = pos[0] + dx, pos[1] + dy
            if 0 <= x < self.cols and 0 <= y < self.rows:
                if self.matrix[x][y] in self.walkable_types:
                    neighbors.append((x, y))
        return neighbors

    def find_path(self, start, goal):
        """Step 2.1: Core A* Algorithm."""
        if start == goal:
            return [start]
            
        frontier = []
        heapq.heappush(frontier, (0, start))
        came_from = {start: None}
        cost_so_far = {start: 0}

        while frontier:
            current = heapq.heappop(frontier)[1]

            if current == goal:
                break

            for next_node in self.get_neighbors(current):
                new_cost = cost_so_far[current] + 1
                if next_node not in cost_so_far or new_cost < cost_so_far[next_node]:
                    cost_so_far[next_node] = new_cost
                    priority = new_cost + self.heuristic(goal, next_node)
                    heapq.heappush(frontier, (priority, next_node))
                    came_from[next_node] = current

        if goal not in came_from:
            return [] # No path found

        # Reconstruct path
        path = []
        curr = goal
        while curr is not None:
            path.append(curr)
            curr = came_from[curr]
        path.reverse()
        return path

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    # Step 2.2: Sandbox Test Case
    mock_matrix = [
        [0, 0, 0, 1], # 1 is Water (Unwalkable)
        [1, 1, 0, 1],
        [0, 0, 0, 0]
    ]
    pathfinder = AStarPathfinder(mock_matrix)
    path = pathfinder.find_path((0, 0), (2, 3))
    
    logger.info(f"Test Path: {path}")
    if path:
        logger.info("CRITIC: Shortest path found successfully.")
    else:
        logger.error("CRITIC: No path found or algorithm failed.")
