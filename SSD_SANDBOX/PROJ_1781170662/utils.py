Sure! Below is a potential implementation of the `utils.py` file for utility helpers in Python:

```python
import os

def create_directory(path):
    """
    Create a directory if it doesn't already exist.
    
    :param path: Path to the directory you want to create.
    """
    if not os.path.exists(path):
        os.makedirs(path)

def list_files_in_directory(directory, prefix=None):
    """
    List files in a specified directory.

    :param directory: The