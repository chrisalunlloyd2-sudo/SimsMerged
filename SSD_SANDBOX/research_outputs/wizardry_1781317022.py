```python
def find_city(start, end):
    return {
        'next': (end - 1), # current starting point's index is already at the start of the list
        'prev': (start + 1) // 2, # previous ending point's index is at the start of the list
        'previous': (start,) if start == end else None
    }[0][0] = end

    def update_current(curr):
        return curr[: