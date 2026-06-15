Certainly! Below is a sample of the `utils.py` file for implementing utility helpers in Python:

```python
# PROJ_1781186226/utils.py

import os
import sys
import json
from typing import List, Dict

def get_files(directory: str) -> List[str]:
    """
    Get a list of files (directories and files) within the specified directory.
    
    :param directory: The path to the directory containing the files.