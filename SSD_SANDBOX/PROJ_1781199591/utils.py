Sure! Below is an example of how you might implement utility functions in Python:

```python
# Define the utility helper class
class UtilHelper:
    def __init__(self):
        pass

    # Add a new item to the list
    def add_item(self, item):
        self.items.append(item)

    # Remove an item from the list
    def remove_item(self, index):
        if 0 <= index < len(self.items):
            del self.items[index]

    #