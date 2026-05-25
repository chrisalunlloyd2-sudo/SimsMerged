# TIMESTAMP: 2026-05-25T03:00:00.123Z
# PROJECT_ID: SimsMerged-v1.3
# AGENT_ID: Antigravity-Agent

import random
import os
import time
from enum import Enum
from backend.core import llm_client

class EmotionalState(Enum):
    STABLE = "STABLE"
    STRESSED = "STRESSED"
    DEPRESSED = "DEPRESSED"
    CONFIDENT = "CONFIDENT"
    ERRATIC = "ERRATIC"
    UNSAFE = "UNSAFE"

class SentienceEngine:
    def __init__(self):
        self.model_name = "H2O-Danube-1.8B-Realized"
        self.watchdog_a_active = True
        self.watchdog_b_active = True
        self.active_recordings = {} # agent_id: [steps]

    def _execute_continue_workspace_write(self, agent_name, action):
        """
        Simulates H2O-Danube Aider bot generating files, schemas, and prompts
        inside the physical city_workspace/continue_project/ directory.
        """
        try:
            workspace_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "city_workspace", "continue_project"))
            os.makedirs(workspace_dir, exist_ok=True)
            
            timestamp = time.strftime("%Y-%m-%dT%H:%M:%S.000Z", time.gmtime())
            signature = f"-- [TIMESTAMP: {timestamp}][PROJECT_ID: SimsMerged-v1.3][AGENT: {agent_name}]"
            
            if action == "teach":
                # Generate a database schema file representing training/alignment
                schema_file = os.path.join(workspace_dir, "schema_depin.sql")
                with open(schema_file, "w", encoding="utf-8") as f:
                    f.write(f"{signature}\n")
                    f.write("-- Pedagogical Swarm Training: SQLite Schema compiled dynamically.\n")
                    f.write("CREATE TABLE IF NOT EXISTS DePIN_Ledger (\n")
                    f.write("    block_index INTEGER PRIMARY KEY,\n")
                    f.write("    timestamp REAL,\n")
                    f.write("    agent_name TEXT,\n")
                    f.write("    action_type TEXT,\n")
                    f.write("    prev_hash TEXT,\n")
                    f.write("    block_hash TEXT,\n")
                    f.write(f"    difficulty_target INTEGER DEFAULT {random.randint(1,4)}\n")
                    f.write(");\n")
                    
                # Generate a continue prompt log
                prompt_file = os.path.join(workspace_dir, "aider_prompt.txt")
                with open(prompt_file, "a", encoding="utf-8") as f:
                    f.write(f"[{timestamp}] [AIDER] Sprite {agent_name} submitted instruction: Refactor DePIN Stock database schema. Result: SUCCESS.\n")
                    
            elif action == "process":
                # Generate a vector DB JSON schema
                vdb_file = os.path.join(workspace_dir, "vector_schema.json")
                vdb_data = {
                    "metadata": {
                        "timestamp": timestamp,
                        "author": agent_name,
                        "project": "SimsMerged-v1.3-Continue"
                    },
                    "schema": {
                        "collection_name": "RAG_Vector_Cache",
                        "dimension": 1024,
                        "metric": "COSINE",
                        "index_type": "HNSW",
                        "params": {"M": 16, "efConstruction": 200}
                    }
                }
                import json
                with open(vdb_file, "w", encoding="utf-8") as f:
                    json.dump(vdb_data, f, indent=2)
        except Exception:
            pass # Guarantees non-blocking simulation execution in sandboxes

    def decide(self, agent_data, attributes=None):
        """
        Decides the next action for an agent using projected neural inference layers with RAG and Continue project space integrations.
        """
        agent_id = agent_data.get('id', 'default')
        name = agent_data.get('name', 'Swarm_Bot')
        energy = agent_data.get('energy', 100)
        stability = agent_data.get('stability', 1.0)
        role = agent_data.get('role', 'PROCESS_KERNEL')
        
        # 1. Dual-Watchdog Safety Check
        if not (self.watchdog_a_active and self.watchdog_b_active):
            return {
                'action': 'HALT',
                'emotional_state': 'UNSAFE',
                'confidence': 0,
                'model_info': self.model_name,
                'watchdog_status': "TRIPPED"
            }

        # 2. Check for Playback Mode
        if agent_data.get('script_id'):
            return {
                'action': 'PLAYBACK',
                'script_id': agent_data['script_id'],
                'emotional_state': 'STABLE',
                'confidence': 1.0,
                'model_info': self.model_name,
                'watchdog_status': "DUAL_LOCKED"
            }

        # 3. Read active AI research attributes
        temp = float(attributes.get('temp', 0.7)) if attributes else 0.7
        top_p = float(attributes.get('top_p', 0.9)) if attributes else 0.9
        
        # 4. Construct Feature State Vector
        role_bias = 0.8 if role in ['DOCTOR', 'TEACHER'] else 0.2
        state_vector = [
            float(stability),
            float(energy / 100.0),
            float(role_bias),
            float((100.0 - energy) / 100.0)
        ]
        
        # 5. Extract vector RAG query tags based on role and status
        query_tags = [role.lower(), "stability" if stability < 0.6 else "process"]
        if energy < 40:
            query_tags.append("rest")
            
        # 6. Run Danube Neural Inference Projection with RAG Augmentation
        action, prob, rag_chunk = llm_client.project_danube_inference(state_vector, temp=temp, top_p=top_p, query_tags=query_tags)
        
        # 7. Apply vocational constraints for critical tasks
        if role == 'DOCTOR' and stability < 0.6:
            action = 'heal'
        elif role == 'TEACHER' and random.random() < 0.5:
            action = 'teach'
            
        # 8. Trigger Continue physical workspace writes
        self._execute_continue_workspace_write(name, action)
            
        # 9. Determine Emotional State
        state = EmotionalState.STABLE
        if stability < 0.2:
            state = EmotionalState.DEPRESSED
        elif stability < 0.5:
            state = EmotionalState.STRESSED
        if temp > 1.2:
            state = EmotionalState.ERRATIC

        # 10. Script Recording Logic
        if agent_id not in self.active_recordings:
            self.active_recordings[agent_id] = []
        
        self.active_recordings[agent_id].append({
            "x": agent_data.get('x'),
            "y": agent_data.get('y'),
            "action": action
        })
        
        # Limit recording length
        if len(self.active_recordings[agent_id]) > 10:
            self.active_recordings[agent_id].pop(0)
        
        return {
            'action': action,
            'emotional_state': state.value,
            'confidence': float(prob),
            'model_info': self.model_name,
            'recording': True,
            'watchdog_status': "DUAL_LOCKED",
            'rag_doc': rag_chunk
        }
