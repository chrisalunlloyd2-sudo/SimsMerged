# [TIMESTAMP: 2026-06-11T20:10:00.000Z] [PROJECT_ID: SimsMerged-v1.4.2] [AGENT_ID: viper_cli-architectssj4]
# Step 41: Genetically Advanced Tok Tree (RAG Context Wrapper)

import json
import os
import time

class TokTree:
    """
    Genetically advanced SSD-fenced Tok Tree (RAG Context Wrapper).
    Provides sub-millisecond context retrieval for the local SLM inference cycle.
    """
    def __init__(self, storage_dir="C:\\Users\\viper\\Desktop\\SimsMerged\\SSD_SANDBOX\\tok_tree_data"):
        self.storage_dir = storage_dir
        if not os.path.exists(self.storage_dir):
            os.makedirs(self.storage_dir)
        self.tree_file = os.path.join(self.storage_dir, "tok_tree.json")
        self.tree_data = {"nodes": []}
        self.load_tree()

    def load_tree(self):
        if os.path.exists(self.tree_file):
            try:
                with open(self.tree_file, "r") as f:
                    self.tree_data = json.load(f)
            except Exception:
                self.tree_data = {"nodes": []}
        else:
            self.tree_data = {"nodes": []}

    def save_tree(self):
        with open(self.tree_file, "w") as f:
            json.dump(self.tree_data, f, indent=4)

    def insert_context(self, context_str, tags):
        """Ingests new context into the SSD-fenced Tok Tree."""
        node = {
            "id": f"node_{len(self.tree_data['nodes'])}",
            "context": context_str,
            "tags": tags,
            "timestamp": time.time()
        }
        self.tree_data["nodes"].append(node)
        self.save_tree()
        return node["id"]

    def augment_prompt(self, prompt, tags):
        """Retrieves matching context and augments the SLM prompt."""
        results = []
        query_tags = set(tags)

        for node in self.tree_data["nodes"]:
            match_score = len(set(node.get("tags", [])).intersection(query_tags))
            if match_score > 0:
                results.append((match_score, node))

        if not results:
            return prompt

        results.sort(key=lambda x: x[0], reverse=True)
        # Take top 3 context nodes
        top_contexts = [r[1]["context"] for r in results[:3]]

        augmented_prompt = (
            "--- SYSTEM CONTEXT (TOK TREE) ---\n"
            + "\n".join(top_contexts) +
            "\n--- END CONTEXT ---\n\n"
            + prompt
        )
        return augmented_prompt

tok_tree = TokTree()