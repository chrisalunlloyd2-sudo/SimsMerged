Sure! Below is an example of how you can implement the `utils.py` file for `PATCH_STABLE_PRO` in Python:

```python
import os

# Define constants and variables for the application
APP_NAME = "patch_stable_pro"
PROG_PATH = os.path.join(os.getcwd(), APP_NAME)
CONFIG_FILE = os.path.join(PROG_PATH, "config.json")

class ConfigHelper:
    def __init__(self):
        self.config_file_path = CONFIG_FILE

    def