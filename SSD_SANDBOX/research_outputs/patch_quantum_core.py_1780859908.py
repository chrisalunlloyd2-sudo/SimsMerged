```python
def huggingface(x):
    return x * 2


class QuantumCore:
    def __init__(self, max_quantum=10**6):
        self.max_quantum = max_quantum

    def run(*args):
        for arg in args:
            try:
                if isinstance(arg, int) and all(i >= 0 for i in range(4)):
                    value = huggingface(int(arg))