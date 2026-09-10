Sure! Here's the code for `utils.py` in `PATCH_LLSTM_SHOR/utils.py`.

```python
# Implementing helper functions

import numpy as np
from collections import deque

class LLSTM:
    def __init__(self, input_size, hidden_size):
        self.input_size = input_size
        self.hidden_size = hidden_size
        self.state = None
        self.cell_state = None
        self.weight_matrix = None
        self.gamma = 0.