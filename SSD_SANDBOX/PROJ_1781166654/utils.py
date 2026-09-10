Certainly! Below is the code for some utility helper functions defined in the file `utils.py`.

```python
# Define utility helpers

def safe_divide(a, b):
    """
    Divide two numbers and handle potential division by zero errors.
    
    Parameters:
        a (float): The numerator of the division.
        b (float): The denominator of the division.
        
    Returns:
        float: The result of the division if successful, None otherwise.
    """
    try:
        return