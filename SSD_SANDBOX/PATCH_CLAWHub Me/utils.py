Sure! Below is an example of how you might implement some utility functions using Python's `patch_clawhub` package.

```python
import patch_clawhub

class PatchCLawHub:
    def __init__(self, api_key):
        self.api_key = api_key

    def get_highest_bid(self, market_code: str) -> dict:
        """Get the highest bid for a given market code."""
        response = patch_clawhub.get_highest_bid(market_code