Certainly! I'll create a helper file called `utils.py` with some utility functions that can be used across different parts of the codebase. This will help in reducing redundancy and making your code more maintainable.

```python
# utils.py

def is_even(number):
    """
    Check if a number is even.
    
    Args:
        number (int): The number to check.
        
    Returns:
        bool: True if the number is even, False otherwise.
    """
    return