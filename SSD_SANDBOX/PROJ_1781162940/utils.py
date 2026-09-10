Certainly! Below is the Python code for `utils.py`, which appears to be a collection of utility functions used in your program or project.

```python
import os

def get_file_size(file_path):
    """
    Get the size (in bytes) of a file.
    
    Args:
        file_path (str): The path to the file.
    
    Returns:
        int: The size of the file in bytes.
    """
    if not os.path.isfile(file_path):
        raise ValueError