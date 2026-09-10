Sure! Here's an implementation of the `utils.py` file in Python:

```python
import requests

class PatchSlowNetwo:
    def __init__(self, url, method='PATCH', data=None):
        self.url = url
        self.method = method
        self.data = data

    def send(self):
        headers = {
            'Content-Type': 'application/json',
        }
        response = requests.request(
            self.method,
            self.url,
            json=self.data