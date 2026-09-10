Sure! Below is the implementation of `utils.py`:

```python
# This module contains utility functions and constants used throughout the application.

import os

def get_current_directory():
    return os.path.abspath(os.path.dirname(__file__))

def get_project_root():
    project_dir = os.environ.get('PROJECT_ROOT', get_current_directory())
    if not os.path.isabs(project_dir):
        project_dir = os.path.join(os.getcwd(), project_dir)
    return project_dir

def get_project_name