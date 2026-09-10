```python
def decay_stability(distance_from_core):
    if distance_from_core < 10:
        return "stability_decay_value_1"
    
    if distance_from_core >= 25 and distance_from_core <= 40:
        return "stability_decay_value_2"
    
    if distance_from_core > 60:
        return "stability_decay_value_3"

    return "unknown_stability_decay"
```