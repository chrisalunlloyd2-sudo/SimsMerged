To implement the utility functions in `PROJ_1781176982/utils.py`, we'll start by defining some basic utilities and then demonstrate how to use them. We will also cover a couple of example scenarios.

### Step 1: Define Basic Utility Functions

Let's define a few common utility functions that are useful in various parts of our application.

```python
import numpy as np

def add_vectors(vec1, vec2):
    return [a + b