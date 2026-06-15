Hello! It looks like you've encountered a syntax error in your code snippet. I'll be happy to help you resolve it and ensure the execution of your script is correct.

Here's the corrected version of your script:

```python
import os

def main():
    patch_path = "HIGH/main.py"
    
    # Check if file exists
    if not os.path.exists(patch_path):
        print(f"Patch file {patch_path} does not exist.")
    else:
        try: