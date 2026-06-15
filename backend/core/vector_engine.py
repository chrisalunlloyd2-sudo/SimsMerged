# TIMESTAMP: 2026-06-03T22:15:00.000Z
# PROJECT_ID: SimsMerged-v1.4-Metropolis
# AGENT_ID: Gemini-CLI-Architect

import json
import os
import urllib.request
import math

class VectorEngine:
    def __init__(self, model="smollm:135m"):
        self.model = model
        self.storage_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "data", "vector_store.json"))
        self.vectors = []
        self.load_store()

    def load_store(self):
        if os.path.exists(self.storage_path):
            try:
                with open(self.storage_path, "r", encoding="utf-8") as f:
                    self.vectors = json.load(f)
            except:
                self.vectors = []

    def save_store(self):
        os.makedirs(os.path.dirname(self.storage_path), exist_ok=True)
        with open(self.storage_path, "w", encoding="utf-8") as f:
            json.dump(self.vectors, f, indent=2)

    def get_embedding(self, text):
        try:
            # Force IPv4 to avoid IPv6 issues
            req = urllib.request.Request("http://127.0.0.1:11434/api/embeddings", headers={"Content-Type": "application/json"})
            data = json.dumps({"model": self.model, "prompt": text}).encode('utf-8')
            with urllib.request.urlopen(req, data=data, timeout=10.0) as response:
                result = json.loads(response.read().decode('utf-8'))
                return result.get('embedding')
        except Exception as e:
            print(f"[VECTOR_ERR] Embedding failed: {e}")
            return None

    def add_document(self, text, metadata=None):
        embedding = self.get_embedding(text)
        if embedding:
            self.vectors.append({
                "text": text,
                "embedding": embedding,
                "metadata": metadata or {}
            })
            self.save_store()

    def search(self, query, top_k=3):
        query_embedding = self.get_embedding(query)
        if not query_embedding or not self.vectors:
            return []

        results = []
        for doc in self.vectors:
            doc_emb = doc["embedding"]
            # Cosine similarity calculation in plain Python
            dot_product = sum(a * b for a, b in zip(query_embedding, doc_emb))
            norm_a = math.sqrt(sum(a * a for a in query_embedding))
            norm_b = math.sqrt(sum(b * b for b in doc_emb))
            similarity = dot_product / (norm_a * norm_b) if norm_a > 0 and norm_b > 0 else 0
            results.append((similarity, doc))

        results.sort(key=lambda x: x[0], reverse=True)
        return results[:top_k]

vector_engine = VectorEngine()
