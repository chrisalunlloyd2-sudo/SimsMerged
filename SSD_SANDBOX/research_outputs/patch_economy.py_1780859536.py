Sure! Let's start with an efficient `economy.py` code:

```python
class Economy:
    def __init__(self):
        self.inventory = {}

    def purchase(self, item_id, quantity):
        if item_id in self.inventory:
            self.inventory[item_id] += quantity
            return f"Successfully purchased {quantity} of `{item_id}`"
        else:
            raise ValueError(f"{item_id} not found.")

    def sell(self, item_id, quantity):