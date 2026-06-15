Certainly! Below is the implementation of `utils.py`, which contains utility functions that can be used across different parts of my codebase. I'll provide some sample usage and explanations along with examples.

```python
import os

def add_to_dict(data, key, value):
    """ Add a new item to a dictionary """
    if isinstance(data, dict):
        data[key] = value
    else:
        data.setdefault(key, value)

def update_with_condition(condition, action, value):