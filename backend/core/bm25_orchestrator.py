# [TIMESTAMP: 2026-06-14T14:15:00.000Z] [PROJECT_ID: SimsMerged-v1.4.2] [AGENT_ID: viper_cli-architectssj4]
# ACTION: Dual BM25 Scaffolding with Persistent "BM100" Logic Weighting

import math
from collections import Counter
import os
import time
import json
from .config import SSD_SANDBOX_PATH, add_log

class AdvancedBM25Orchestrator:
    """
    Offline lexical search orchestrator.
    Supports DYNAMIC LEARNING and Persistent Storage.
    Implements 'BM100' logic: A Lean Six Sigma multiplier based on code deterministic quality.
    """
    def __init__(self, namespace="default", k1=1.5, b=0.75):
        self.namespace = namespace
        self.db_path = os.path.join(SSD_SANDBOX_PATH, f"bm25_{self.namespace}.json")
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
        self._load()

    def _load(self):
        if os.path.exists(self.db_path):
            try:
                with open(self.db_path, "r", encoding="utf-8") as f:
                    self.documents = json.load(f)
                self._recompute_statistics()
            except Exception as e:
                add_log(f"[BM25_{self.namespace.upper()}] Load failed: {e}", "warning")

    def _save(self):
        try:
            with open(self.db_path, "w", encoding="utf-8") as f:
                json.dump(self.documents, f, indent=2)
        except Exception as e:
            add_log(f"[BM25_{self.namespace.upper()}] Save failed: {e}", "warning")

    def ingest_corpus(self, docs_with_metadata):
        """Ingests a list of dictionaries: [{'id': 1, 'text': '...', 'tags': [...], 'lss_weight': 1.0}]"""
        self.documents.extend(docs_with_metadata)
        self._recompute_statistics()
        self._save()

    def update_learning(self, new_text, metadata=None):
        """Dynamic Pedagogy: Learn from a new piece of code or thought."""
        doc = {"id": f"L{len(self.documents)+1}", "text": new_text, "timestamp": time.time(), "lss_weight": 1.0}
        if metadata: doc.update(metadata)
        self.documents.append(doc)
        self._recompute_statistics()
        self._save()
        add_log(f"[BM25_{self.namespace.upper()}] Absorbed new knowledge: {new_text[:40]}...")

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
                    base_score = q_idf * f * (self.k1 + 1) / (f + self.k1 * (1 - self.b + self.b * len(doc) / self.avgdl))
                    # "BM100" Ascension multiplier: Apply Lean Six Sigma weight
                    lss_mult = self.documents[i].get('lss_weight', 1.0)
                    scores[i] += (base_score * lss_mult)
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

class DualBM25Scaffolding:
    """
    Pillar I: Dual-Layered Knowledge Retrieval.
    """
    def __init__(self):
        self.continuity = AdvancedBM25Orchestrator("continuity")
        self.ghost_codes = {} # Subdivided by language

    def get_ghost_code(self, language: str) -> AdvancedBM25Orchestrator:
        lang = language.lower()
        if lang not in self.ghost_codes:
            self.ghost_codes[lang] = AdvancedBM25Orchestrator(f"ghostcode_{lang}")
        return self.ghost_codes[lang]

# Global Dual BM25 Engine
bm25_scaffold = DualBM25Scaffolding()

# Legacy alias for backward compatibility until full refactor
bm25_engine = bm25_scaffold.continuity

# Ensure initial knowledge exists in continuity DB
if len(bm25_engine.documents) == 0:
    INITIAL_KNOWLEDGE = [
        {"id": "K1", "text": "ReAct workflow reasons about a problem, acts using tools, and observes the result before continuing.", "lss_weight": 1.2},
        {"id": "K2", "text": "Speculative decoding uses a smaller draft model to predict tokens, which a larger model verifies in parallel.", "lss_weight": 1.1},
        {"id": "K3", "text": "KV Caching saves key and value tensors from self-attention layers to prevent recomputation.", "lss_weight": 1.0},
        {"id": "K4", "text": "Aider style commits involve making surgical AST changes and immediately executing a git commit.", "lss_weight": 1.5},
        {"id": "K5", "text": "SimAgentCity deterministic database layout maps genetic SOPs, task XP, and SLM weights across decentralized hubs.", "lss_weight": 1.8},
        {"id": "K6", "text": "Metropolis Authority FastAPI backend utilizes multi-threaded background loops to process PoW block validations safely.", "lss_weight": 1.3},
        {"id": "K7", "text": "Danube Coin (DANUBE_COIN) serves as a stable local tokenomic anchor, fluctuates based on global environment stability indexes.", "lss_weight": 1.4}
    ]
    bm25_engine.ingest_corpus(INITIAL_KNOWLEDGE)
