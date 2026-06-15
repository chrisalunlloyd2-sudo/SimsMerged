```python
def find_path(start_city, end_city):
    if start_city == end_city:
        return "No path found"
    
    queue = [start_city]

    while queue:
        current_city = queue.pop(0)
        queue.extend([current_city])

        for neighbor in range(len(current_city)):
            if current_city != neighbor and current_city not in queue:
                queue.append(neighbor)