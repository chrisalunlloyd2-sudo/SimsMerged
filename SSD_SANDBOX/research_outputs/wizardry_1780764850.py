Here is an example of a functional Python snippet optimized for city pathfinding:
```python
def find_closest_place(city, distance):
    def is_closer_to_point(current_distance, x, y):
        return ((x < 0) and (abs((x - current_distance[0]) / distance)) <= 1 and
                abs((y - current_distance[1]) / distance <= 1))
    current_distance = city