# [TIMESTAMP: 2026-06-11T04:40:00.000Z] [PROJECT_ID: SimsMerged-v1.4.2] [AGENT_ID: Gemini-CLI-Architect]

import numpy as np
import pickle
import os
from typing import List, Tuple, Dict

class LSTMScratch:
    """
    PHASE 30: PURE NUMPY LSTM FROM SCRATCH
    - Predictive code 'autocomplete' engine.
    - Manages hidden state (h) and cell state (c) across time steps.
    - Trained on high-quality code snippets.
    """
    def __init__(self, input_dim: int, hidden_dim: int, output_dim: int):
        self.input_dim = input_dim
        self.hidden_dim = hidden_dim
        self.output_dim = output_dim

        # Weights Initialization (Xavier/Glorot)
        self.Wf = np.random.randn(hidden_dim, hidden_dim + input_dim) * 0.1
        self.Wi = np.random.randn(hidden_dim, hidden_dim + input_dim) * 0.1
        self.Wc = np.random.randn(hidden_dim, hidden_dim + input_dim) * 0.1
        self.Wo = np.random.randn(hidden_dim, hidden_dim + input_dim) * 0.1
        self.Wy = np.random.randn(output_dim, hidden_dim) * 0.1

        self.bf = np.zeros((hidden_dim, 1))
        self.bi = np.zeros((hidden_dim, 1))
        self.bc = np.zeros((hidden_dim, 1))
        self.bo = np.zeros((hidden_dim, 1))
        self.by = np.zeros((output_dim, 1))

    def sigmoid(self, x):
        return 1 / (1 + np.exp(-x))

    def tanh(self, x):
        return np.tanh(x)

    def softmax(self, x):
        e_x = np.exp(x - np.max(x))
        return e_x / e_x.sum(axis=0)

    def forward(self, x_seq: List[np.ndarray]) -> Tuple[List[np.ndarray], List[np.ndarray], List[np.ndarray]]:
        """Forward pass through time."""
        h = np.zeros((self.hidden_dim, 1))
        c = np.zeros((self.hidden_dim, 1))
        
        hs, cs, caches = [], [], []
        
        for x in x_seq:
            x = x.reshape(-1, 1)
            concat = np.vstack((h, x))
            
            f = self.sigmoid(np.dot(self.Wf, concat) + self.bf)
            i = self.sigmoid(np.dot(self.Wi, concat) + self.bi)
            c_tilde = self.tanh(np.dot(self.Wc, concat) + self.bc)
            
            c = f * c + i * c_tilde
            o = self.sigmoid(np.dot(self.Wo, concat) + self.bo)
            h = o * self.tanh(c)
            
            y = self.softmax(np.dot(self.Wy, h) + self.by)
            
            hs.append(h)
            cs.append(c)
            caches.append((concat, f, i, c_tilde, c, o, y))
            
        return hs, cs, caches

    def predict(self, x_seq: List[np.ndarray]) -> np.ndarray:
        hs, cs, caches = self.forward(x_seq)
        return caches[-1][-1] # Return the last softmax output

    def save(self, path: str):
        with open(path, 'wb') as f:
            pickle.dump(self.__dict__, f)

    @classmethod
    def load(cls, path: str):
        with open(path, 'rb') as f:
            data = pickle.load(f)
        obj = cls(data['input_dim'], data['hidden_dim'], data['output_dim'])
        obj.__dict__.update(data)
        return obj

class CodeTokenizer:
    """Simple character-level tokenizer for the LSTM."""
    def __init__(self):
        self.char_to_ix = {}
        self.ix_to_char = {}
        self.vocab_size = 0

    def fit(self, text: str):
        chars = sorted(list(set(text)))
        self.char_to_ix = {ch: i for i, ch in enumerate(chars)}
        self.ix_to_char = {i: ch for i, ch in enumerate(chars)}
        self.vocab_size = len(chars)

    def encode(self, text: str) -> List[np.ndarray]:
        vecs = []
        for ch in text:
            v = np.zeros((self.vocab_size, 1))
            v[self.char_to_ix.get(ch, 0)] = 1
            vecs.append(v)
        return vecs

    def decode(self, ix: int) -> str:
        return self.ix_to_char.get(ix, '')
