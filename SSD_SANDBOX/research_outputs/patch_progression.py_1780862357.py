Here is how to implement this hot-patch:
```python
def hot_patch(func):
    optimize = func.__name__[:-3]  # Remove "optimize" from the function name
    if optimize not in ["progression", "optimizer"]:
        raise ValueError('Optimized function must not end with 'optimize')
    def wrapper(*args, **kwargs):
        exec(f"def {optimize}({args}, {kwargs})")
        return func(*args, **kwargs