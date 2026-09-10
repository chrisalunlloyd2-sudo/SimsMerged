Sure! Below is the `utils.py` file for creating some utility functions in Python:

```python
# Import any necessary packages here

def calculate_average(numbers):
    """
    Calculate the average of a list of numbers.
    
    Args:
        numbers (list): A list of numeric values.
        
    Returns:
        float: The average of the numbers.
    """
    if not numbers:
        return 0.0
    else:
        return sum(numbers) / len(numbers)

def