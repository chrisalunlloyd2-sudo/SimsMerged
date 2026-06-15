# [TIMESTAMP: 2026-06-11T02:45:00.000Z] [PROJECT_ID: SimsMerged-v1.4.2] [AGENT_ID: Gemini-CLI-Architect]

import chromadb
import os
import json
import hashlib
from typing import List, Dict, Optional
from .config import SSD_SANDBOX_PATH

VECTOR_DB_PATH = os.path.join(SSD_SANDBOX_PATH, "vector_ring")

class VectorRingDB:
    """
    PHASE 24: THE VECTOR RING (SOVEREIGN MEMORY)
    - Stores high-dimensional embeddings of code blocks, patterns, and research.
    - Enables semantic 'Symbolic Routing' to prevent redundant synthesis.
    - Layered by programming language and performative category.
    """
    def __init__(self):
        self.client = chromadb.PersistentClient(path=VECTOR_DB_PATH)
        self.collection = self.client.get_or_create_collection(name="logic_ring")

    def store_pattern(self, code: str, language: str, performative: str, metadata: Dict = None):
        """Adds a code block to the ring with metadata layers."""
        block_id = hashlib.sha256(code.encode()).hexdigest()[:16]
        
        meta = metadata or {}
        meta.update({
            "language": language,
            "performative": performative,
            "hash": block_id
        })
        
        self.collection.add(
            documents=[code],
            metadatas=[meta],
            ids=[block_id]
        )
        print(f"🌀 [VECTOR_RING] Pattern {block_id} cached in {language} layer.")

    def query_logic(self, prompt: str, language: str = None, top_k: int = 1) -> List[Dict]:
        """Searches for existing logic templates matching the prompt."""
        where = {"language": language} if language else {}
        
        results = self.collection.query(
            query_texts=[prompt],
            n_results=top_k,
            where=where
        )
        
        logic_matches = []
        if results['documents'] and len(results['documents'][0]) > 0:
            for i in range(len(results['documents'][0])):
                logic_matches.append({
                    "code": results['documents'][0][i],
                    "metadata": results['metadatas'][0][i],
                    "distance": results['distances'][0][i]
                })
        return logic_matches

vector_ring = VectorRingDB()
