Sure! Below is an example of how you can implement the `utils.py` file for utility helpers in Python:

```python
# utils.py

def sum_of_squares(numbers):
    """
    Calculate the sum of squares of a list of numbers.
    
    Args:
        numbers (list): A list of numeric values.

    Returns:
        float: The sum of squares of the given numbers.
    """
    if not numbers:
        return 0.0
    else:
        total