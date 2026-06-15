Sure! Below is the implementation of `utils.py` that contains utility functions:

```python
import math

def is_prime(num):
    """
    Check if a number is prime.
    
    Args:
        num (int): The number to check.
        
    Returns:
        bool: True if the number is prime, False otherwise.
    """
    if num <= 1:
        return False
    for i in range(2, int(math.sqrt(num)) + 1):
        if