Certainly! I'll write the Python code for the "Logic Engine" part of your project. This code will help you implement a simple logic engine that can perform basic logical operations like AND, OR, and NOT.

First, let's define the necessary classes:

```python
import pandas as pd

class LogicEngine:
    def __init__(self):
        self.data = None  # Assume this is your DataFrame with boolean values

    def add(self, condition_str, value):
        """