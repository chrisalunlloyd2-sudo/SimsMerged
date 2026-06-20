# [PERFORMATIVE: SCOUT_AGENT]
import json
import logging

def scout_decompose_goals(world_map_json, global_goal):
    """Decomposes a large goal (e.g. 'Build Cabin') into micro-tasks."""
    # 1. Parse Map
    with open(world_map_json, 'r') as f:
        world = json.load(f)

    # 2. Logic: If goal is Build Cabin, we need Wood and Stone.
    # Find coordinates of Wood (Terrain 0) and Stone (Terrain 2).
    tasks = []
    for x in range(10):
        for y in range(10):
            tile = world['matrix'][x][y]
            if tile == 0: tasks.append({"type": "GATHER", "item": "Wood", "coord": (x,y)})
            if tile == 2: tasks.append({"type": "GATHER", "item": "Stone", "coord": (x,y)})
            if len(tasks) >= 5: break
        if len(tasks) >= 5: break

    return tasks
