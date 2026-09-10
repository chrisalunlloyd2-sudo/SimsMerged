# [TIMESTAMP: 2026-06-14T17:15:00.000Z]
import sys
import os

project_root = r"C:\Users\viper\Desktop\SimsMerged"
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from backend.core.bm25_orchestrator import bm25_scaffold

def test_search():
    query = "Establish Evolution Heartbeat"
    results = bm25_scaffold.continuity.search(query, top_k=3)
    print(f"Results for '{query}':")
    for doc, score in results:
        print(f"Score: {score:.2f} | Text: {doc['text'][:100]}...")

if __name__ == "__main__":
    test_search()
