Certainly! I'll provide you with a simple example of how to implement `utils.py` in Python. This example will have basic utility functions for common tasks.

### Example: Function to Convert Bytes to Hexadecimal

Here's an implementation of a function that converts a 32-bit unsigned integer (big-endian) into a hexadecimal string:

```python
def int_to_hex(num):
    return hex(num)[2:]

# Usage:
print(int_to_hex(10))  # Output: