Certainly! Below is a sample implementation of utility helper functions in Python that can be used to simplify common tasks or utilities:

```python
import numpy as np

def average(values):
    """
    Calculates the average of a list of numbers.

    Parameters:
        values (list): A list of numerical values.

    Returns:
        float: The average value.
    """
    return sum(values) / len(values)

def mean_squared_error(y_true, y_pred):
    """
    Calculates the Mean Squ