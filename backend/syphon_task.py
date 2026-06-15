# TIMESTAMP: 2026-06-09
import sys
import os

sys.path.insert(0, r"C:\Users\viper\Desktop\SimsMerged")
from backend.sprite_triplet.pedagogy_memory import HybridCodeSearch

memory = HybridCodeSearch()
with open(r'C:\Users\viper\Desktop\SimsMerged\backend\world_genesis.py', 'r') as f:
    code = f.read()
memory.ingest_code(code, 'Flash-Lite', 1.0)
print("Syphon Complete.")
