# [TIMESTAMP: 2026-06-07T15:30:00.000Z] [PROJECT_ID: SimsMerged-v1.4.2] [AGENT_ID: Gemini-CLI-Architect]

import math
from collections import Counter
import sqlite3
import os
import json
from .config import AGENT_MEMORIES_DIR

class SimpleBM25:
    """Dependency-free BM25 implementation for SSD-fenced RAG."""
    def __init__(self, corpus):
        self.corpus_size = len(corpus)
        self.avgdl = sum(len(doc) for doc in corpus) / self.corpus_size if self.corpus_size else 0
        self.doc_freqs = []
        self.idf = {}
        self.doc_len = []
        self.k1 = 1.5
        self.b = 0.75
        self._initialize(corpus)

    def _initialize(self, corpus):
        df = {}
        for doc in corpus:
            self.doc_len.append(len(doc))
            counts = Counter(doc)
            self.doc_freqs.append(counts)
            for word in counts:
                df[word] = df.get(word, 0) + 1
        for word, freq in df.items():
            self.idf[word] = math.log(1 + (self.corpus_size - freq + 0.5) / (freq + 0.5))

    def get_scores(self, query):
        scores = [0] * self.corpus_size
        for q in query:
            if q not in self.idf: continue
            idf = self.idf[q]
            for i, doc in enumerate(self.doc_freqs):
                f = doc.get(q, 0)
                scores[i] += idf * (f * (self.k1 + 1)) / (f + self.k1 * (1 - self.b + self.b * self.doc_len[i] / self.avgdl))
        return scores

class LLSTMDatabase:
    """
    Long Short-Term Memory (LLSTM) pattern using BM25.
    Attaches to each individual local model's memory.
    """
    def __init__(self, agent_id):
        self.agent_id = agent_id
        self.db_path = os.path.join(AGENT_MEMORIES_DIR, f"{agent_id}.db")

    def retrieve_llstm_context(self, current_query, short_term_limit=3, long_term_limit=2):
        """Combines short-term sequential memory with long-term BM25 associative memory."""
        if not os.path.exists(self.db_path):
            return "LLSTM: INITIALIZED_BLANK"

        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        # 1. Short-Term (Rolling)
        cursor.execute('SELECT action, context, response FROM memories ORDER BY id DESC LIMIT ?', (short_term_limit,))
        short_term_rows = cursor.fetchall()[::-1]

        # 2. Long-Term (BM25)
        cursor.execute('SELECT id, context, response FROM memories')
        all_rows = cursor.fetchall()
        conn.close()

        long_term_hits = []
        if all_rows and current_query:
            corpus = [str(r[1]).lower().split() + str(r[2]).lower().split() for r in all_rows]
            bm25 = SimpleBM25(corpus)
            query_tokens = current_query.lower().split()
            scores = bm25.get_scores(query_tokens)

            # Get top indices
            top_indices = sorted(range(len(scores)), key=lambda i: scores[i], reverse=True)[:long_term_limit]
            for idx in top_indices:
                if scores[idx] > 0:
                    long_term_hits.append(all_rows[idx])

        # Combine into LLSTM Block
        context_block = "\\n[LLSTM_SHORT_TERM]: "
        for m in short_term_rows:
            context_block += f"{m[0]}|{m[1][:15]}..|{m[2][:20]}.. "

        context_block += "\\n[LLSTM_LONG_TERM_BM25]: "
        for m in long_term_hits:
            context_block += f"RECALL_ID_{m[0]}: {m[2][:30]}.. "

        return context_block
