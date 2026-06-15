Sure! Below is the `utils.py` file that contains utility helpers:

```python
# This file contains utility functions and constants.

import os
import json

def read_json_file(file_path):
    """
    Read a JSON file and return its content.
    
    Parameters:
        file_path (str): The path to the JSON file.
        
    Returns:
        dict: The content of the JSON file as a Python dictionary.
    """
    with open(file_path, 'r') as file