# [TIMESTAMP: 2026-06-02T04:03:30.452Z] [PROJECT_ID: SimsMerged-v1.4-Metropolis] [AGENT_ID: Antigravity-CLI-Architect]
# ACTION: Dynamic BM25 Orchestrator with Real-Time Learning

import math
from collections import Counter
import os
import time

class BM25Orchestrator:
    """
    Offline lexical search orchestrator. 
    Boosts Agy's context by analyzing ViperNotes and local workspaces in milliseconds.
    Supports DYNAMIC LEARNING: Updates corpus as agents work.
    """
    def __init__(self, k1=1.5, b=0.75):
        self.k1 = k1
        self.b = b
        self.corpus = []
        self.documents = []
        self.corpus_size = 0
        self.avgdl = 0
        self.f = []
        self.df = {}
        self.idf = {}
        self.is_initialized = False

    def ingest_corpus(self, docs_with_metadata):
        """Ingests a list of dictionaries: [{'id': 1, 'text': '...', 'tags': [...]}]"""
        self.documents.extend(docs_with_metadata)
        self._recompute_statistics()

    def update_learning(self, new_text, metadata=None):
        """Dynamic Pedagogy: Learn from a new piece of code or thought."""
        doc = {"id": f"L{len(self.documents)+1}", "text": new_text, "timestamp": time.time()}
        if metadata: doc.update(metadata)
        self.documents.append(doc)
        self._recompute_statistics()
        print(f"[BM25 LEARNING] Absorbed new knowledge: {new_text[:50]}...")

    def _recompute_statistics(self):
        self.corpus = [doc['text'].lower().split() for doc in self.documents]
        self.corpus_size = len(self.corpus)
        if self.corpus_size == 0:
            return
            
        self.avgdl = sum(len(doc) for doc in self.corpus) / self.corpus_size
        self.f = []
        self.df = {}
        self.idf = {}

        for document in self.corpus:
            frequencies = Counter(document)
            self.f.append(frequencies)
            for word in frequencies:
                if word not in self.df:
                    self.df[word] = 0
                self.df[word] += 1

        for word, freq in self.df.items():
            # Standard BM25 IDF with smoothing
            self.idf[word] = math.log((self.corpus_size - freq + 0.5) / (freq + 0.5) + 1)
            
        self.is_initialized = True

    def get_scores(self, query):
        if not self.is_initialized or self.corpus_size == 0:
            return []
            
        scores = [0.0] * self.corpus_size
        for q in query:
            q_idf = self.idf.get(q, 0)
            if q_idf != 0:
                for i, doc in enumerate(self.corpus):
                    f = self.f[i].get(q, 0)
                    scores[i] += q_idf * f * (self.k1 + 1) / (f + self.k1 * (1 - self.b + self.b * len(doc) / self.avgdl))
        return scores

    def search(self, query_string, top_k=3):
        query = query_string.lower().split()
        scores = self.get_scores(query)
        if not scores:
            return []
            
        top_indices = sorted(range(len(scores)), key=lambda i: scores[i], reverse=True)[:top_k]
        results = []
        for idx in top_indices:
            if scores[idx] > 0:
                results.append((self.documents[idx], scores[idx]))
        return results

# Global BM25 Instance
bm25_engine = BM25Orchestrator()

INITIAL_KNOWLEDGE = [
    {"id": "K1", "text": "ReAct workflow reasons about a problem, acts using tools, and observes the result before continuing."},
    {"id": "K2", "text": "Speculative decoding uses a smaller draft model to predict tokens, which a larger model verifies in parallel."},
    {"id": "K3", "text": "KV Caching saves key and value tensors from self-attention layers to prevent recomputation."},
    {"id": "K4", "text": "Aider style commits involve making surgical AST changes and immediately executing a git commit."},
    {"id": "K5", "text": "SimAgentCity deterministic database layout maps genetic SOPs, task XP, and SLM weights across decentralized hubs."},
    {"id": "K6", "text": "Metropolis Authority FastAPI backend utilizes multi-threaded background loops to process PoW block validations safely."},
    {"id": "K7", "text": "Danube Coin (DANUBE_COIN) serves as a stable local tokenomic anchor, fluctuates based on global environment stability indexes."}
]
bm25_engine.ingest_corpus(INITIAL_KNOWLEDGE)
