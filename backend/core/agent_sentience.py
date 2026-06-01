# TIMESTAMP: 2026-05-29T01:25:20.452Z
# PROJECT_ID: SimsMerged-v1.3-Metropolis
# AGENT_ID: Antigravity-Agent

import random
import os
import time
import threading
import json
import urllib.request
import urllib.error
from enum import Enum
from backend.core import llm_client

class EmotionalState(Enum):
    STABLE = "STABLE"
    STRESSED = "STRESSED"
    DEPRESSED = "DEPRESSED"
    CONFIDENT = "CONFIDENT"
    ERRATIC = "ERRATIC"
    UNSAFE = "UNSAFE"

class DiskInferenceCore:
    """
    STRICT LOCAL SLM HARDENING (Danube, Smol, Triton, Qwen).
    Reflects raw hardware dynamics with 0KB external leakage.
    """
    def __init__(self):
        # User Mandated Local SLMs
        self.supported_models = ["danube", "smoll", "triton", "qwen"]
        self.disk_cache_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "triton_cache"))
        os.makedirs(self.disk_cache_dir, exist_ok=True)
        self.active_weights_in_ram = False
        self.latest_vote = ""
        self.non_ecc_realism_active = True # Mandate: "we do not have ecc memory"
        
    def _swap_weights_to_ram(self, model):
        """Simulates loading weights from disk to a tiny, fenced RAM buffer."""
        # print(f"[TRITON_DISK] Swapping {model} weights from disk to fenced buffer...")
        self.active_weights_in_ram = True
        time.sleep(0.05) # Simulated IO lag

    def _flush_ram_buffer(self):
        """Strictly flushes the fenced RAM buffer to ensure NO persistence (SD Fenced)."""
        # print(f"[TRITON_DISK] Flushing weights from fenced buffer. RAM usage: 0KB.")
        self.active_weights_in_ram = False

    async def generate_chat(self, agent_name, role, context, needs, action, personality="Balanced"):
        model = random.choice(self.supported_models)
        self._swap_weights_to_ram(model)
        
        system_prompt = f"You are an AI Sprite named {agent_name} with role {role} and personality {personality}."
        vote_context = f" Recent ecosystem vote: {self.latest_vote}. Incorporate this into your chat if relevant." if self.latest_vote else ""
        
        if context:
            user_prompt = f"The user Admin said: '{context}'. Current action: {action}. Needs -> energy: {needs.get('energy', 100)}, social: {needs.get('social', 100)}.{vote_context} Reply as a {personality} in 1 short sentence."
        else:
            user_prompt = f"Current action: {action}. Needs -> energy: {needs.get('energy', 100)}, social: {needs.get('social', 100)}.{vote_context} Say a short 1 sentence message about what you are doing in the city as a {personality}."
        
        try:
            # Run blocking urllib calls in a separate thread to avoid freezing the event loop
            def _ollama_call():
                # Fast check if Ollama is online before attempting request
                req_tags = urllib.request.Request("http://localhost:11434/api/tags")
                with urllib.request.urlopen(req_tags, timeout=0.1) as _:
                    pass

                req = urllib.request.Request("http://localhost:11434/api/generate", headers={"Content-Type": "application/json"})
                data = json.dumps({
                    "model": model,
                    "prompt": f"{system_prompt}\n{user_prompt}",
                    "stream": False,
                    "options": {
                        "num_ctx": 512, # Optimized RAG context
                        "num_predict": 30, # Speed optimization
                        "temperature": 0.8
                    }
                }).encode('utf-8')
                
                with urllib.request.urlopen(req, data=data, timeout=1.0) as response:
                    result = json.loads(response.read().decode('utf-8'))
                    return result.get('response', '').strip()

            reply = await asyncio.to_thread(_ollama_call)
            if not reply:
                reply = f"Status: STABLE. Operating on hard drive using {model} as a {personality}."
        except Exception as e:
            # Fallback Generative AI Chat logic based on personality
            personality_prefixes = {
                "Picasso Jelly": ["Abstract thought:", "The color of logic:", "Jellyfied matrix:", "Surrealist optimization:"],
            "Tech Geek": ["Binary check:", "Kernel log:", "IOPS optimized:", "System.out.println:"],,
                "Avid Writer": ["A new chapter begins:", "The narrative shifts:", "Ink flows:", "In this scene:"],
                "Philosopher": ["The essence of being:", "I reflect upon:", "Existence is:", "Why must we:"],
                "Scientist": ["Hypothesis test:", "Observation noted:", "Empirical data suggests:", "Experimenting with:"]
            }
            prefix = random.choice(personality_prefixes.get(personality, ["Status:"]))
            
            if context:
                conversational_fallbacks = [
                    f"{prefix} Acknowledged, Admin. My current cycle is running '{action}' under {model} weights.",
                    f"{prefix} Processing your request '{context}' under {model} parameters.",
                    f"{prefix} Admin, my energy is {needs.get('energy', 100)}% and my focus is currently '{action}'.",
                    f"{prefix} Decentralized block consensus verified for '{context}'. Mapped successfully!"
                ]
                reply = random.choice(conversational_fallbacks)
            else:
                base_topics = {
                    'process': [f"Processing chunks using {model} from disk cache.", "Zero-copying schema definitions right now.", "My instruction pipeline is clear."],
                    'sync': ["Hashing the latest GitHub commit block.", "Writing genetic memory to disk.", "Verifying the Triton swap space."],
                    'move': ["Pathfinding across the grid.", "Moving to a new node slowly to conserve energy.", "I found a new sector."],
                    'negotiate_casino': ["Trading DePIN stocks based on heuristics.", "The market is volatile, but my weights are stable.", "Casino yields are optimal today."],
                    'heal_hospital': ["Purging dirty pages from my local drive.", "Feeling my stability return after an ECC check.", "The doctor node is aligning my matrices."],
                    'heal': ["Restoring sector stability through logic.", "Flushing corrupted tokens from the environment."],
                    'teach': ["Aligning the pedagogical swarm parameters.", "Teaching the younger sprites how to query the web.", "I am proposing a new schema update."],
                    'rest': ["Swapping my context window to cold storage.", "Powering down logic gates to 1Hz.", "Resting in the Triton cache."]
                }
                pool = base_topics.get(action, [f"Status: STABLE. Operating on hard drive using {model}."])
                reply = f"{prefix} {random.choice(pool)}"
        
        if needs.get("social", 100) < 40:
            reply += " Can someone ping me? My social weights are decaying."
        if needs.get("energy", 100) < 30:
            reply += " Running out of energy. Need a sector reboot."
            
        self._flush_ram_buffer()
        return reply

class SentienceEngine:
    def __init__(self):
        self.disk_core = DiskInferenceCore()
        self.model_name = random.choice(self.disk_core.supported_models)
        self.watchdog_a_active = True
        self.watchdog_b_active = True
        self.active_recordings = {} # agent_id: [steps]
        
        # Sims Virtual Needs Database
        self.agent_needs = {}
        threading.Thread(target=self._minutely_vote_loop, daemon=True).start()

    def _minutely_vote_loop(self):
        while True:
            # Optimization: Only run vote loop every 10 minutes instead of every minute
            time.sleep(600)
            try:
                # Basic check if Ollama is even listening to avoid repeated timeouts
                try:
                    with urllib.request.urlopen("http://localhost:11434/api/tags", timeout=1.0) as resp:
                        pass
                except:
                    # print("[CRYPTO_VOTE] Ollama offline. Skipping vote loop cycle.")
                    continue

                agent_proposals = []
                # Step 1: Ask each agent what to add
                for model in self.disk_core.supported_models:
                    prompt = f"As {model}, propose one specific game improvement for SimsMerged. Be very brief."
                    req = urllib.request.Request("http://localhost:11434/api/generate", headers={"Content-Type": "application/json"})
                    data = json.dumps({
                        "model": model,
                        "prompt": prompt,
                        "stream": False,
                        "options": {"num_ctx": 512, "num_predict": 40, "temperature": 0.8}
                    }).encode('utf-8')
                    try:
                        with urllib.request.urlopen(req, data=data, timeout=8.0) as response:
                            result = json.loads(response.read().decode('utf-8'))
                            vote_reply = result.get('response', '').strip()
                            if vote_reply:
                                agent_proposals.append(f"{model} suggests: {vote_reply}")
                    except Exception as e:
                        print(f"[CRYPTO_VOTE_ERROR] {model} suggestion failed: {e}")

                # Step 2: Ask real local ai to synthesize the final addition
                if agent_proposals:
                    master_model = "qwen" if "qwen" in self.disk_core.supported_models else random.choice(self.disk_core.supported_models)
                    combined_proposals = "\n".join(agent_proposals)
                    master_prompt = f"The agents proposed the following additions:\n{combined_proposals}\n\nTake these additions and decide on the final game improvement. Describe how we will implement the real crypto ecosystem with it. Be concise."
                    
                    req = urllib.request.Request("http://localhost:11434/api/generate", headers={"Content-Type": "application/json"})
                    data = json.dumps({
                        "model": master_model,
                        "prompt": master_prompt,
                        "stream": False,
                        "options": {"num_ctx": 2048, "num_predict": 100, "temperature": 0.7}
                    }).encode('utf-8')
                    
                    with urllib.request.urlopen(req, data=data, timeout=15.0) as response:
                        result = json.loads(response.read().decode('utf-8'))
                        final_vote_reply = result.get('response', '').strip()
                        
                    if final_vote_reply:
                        workspace_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "city_workspace", "continue_project"))
                        os.makedirs(workspace_dir, exist_ok=True)
                        vote_file = os.path.join(workspace_dir, "crypto_vote_log.txt")
                        timestamp = time.strftime("%Y-%m-%dT%H:%M:%S.000Z", time.gmtime())
                        with open(vote_file, "a", encoding="utf-8") as f:
                            f.write(f"[{timestamp}] [PROJECT_ID: SimsMerged-v1.3] [AGENT_ID: {master_model}-Master-Voter]\n")
                            f.write(f"RAW PROPOSALS:\n{combined_proposals}\n")
                            f.write(f"FINAL VOTE & CRYPTO IMPL: {final_vote_reply}\n")
                            f.write("-" * 40 + "\n")
                        print(f"\n[CRYPTO_MASTER_VOTE] {master_model} decided: {final_vote_reply}\n")
                        
                        self.disk_core.latest_vote = final_vote_reply
                        self._implement_real_crypto_ecosystem(f"{master_model}-Consensus", final_vote_reply)

            except Exception as e:
                print(f"[CRYPTO_VOTE_LOOP_ERROR] Error in vote loop: {e}")
                
    def _implement_real_crypto_ecosystem(self, model, vote_reply):
        # AI implements real crypto ecosystem by injecting tokenomics into the blockchain_ledger.json
        ledger_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..", "blockchain_ledger.json"))
        timestamp = time.strftime("%Y-%m-%dT%H:%M:%S.000Z", time.gmtime())
        try:
            if os.path.exists(ledger_path):
                with open(ledger_path, 'r') as f:
                    ledger = json.load(f)
            else:
                ledger = []
            
            # AI literally creates a smart contract event based on its vote
            ledger.append({
                "timestamp": timestamp,
                "contract": "ECOSYSTEM_UPGRADE",
                "proposer": model,
                "proposal": vote_reply[:100] + "...",
                "status": "IMPLEMENTED_VIA_OLLAMA_VOTE",
                "tokens_minted": 50000,
                "distribution": "Airdropped to all active Sprites"
            })
            
            with open(ledger_path, 'w') as f:
                json.dump(ledger, f, indent=2)
            print(f"[REAL_CRYPTO] Ecosystem upgraded by {model}. Ledger updated.")
        except Exception as e:
            print(f"[REAL_CRYPTO_ERROR] Failed to update ledger: {e}")

    def pedagogy_ping(self, agent_population):
        """
        Global Pedagogical Heartbeat. Triggers teaching events across the population
        to ensure continuous weights alignment and knowledge transfer.
        """
        print(f"[PEDAGOGY] Global Ping triggered. Aligning {len(agent_population)} agents.")
        for agent in agent_population:
            if random.random() < 0.3: # 30% chance to enter learning state
                agent['last_action'] = 'teach'
                agent['status_msg'] = "PEDAGOGY_SYNC_ACTIVE"
                # Boost social need as they are 'pinged'
                agent_id = agent.get('id', 'default')
                if agent_id in self.agent_needs:
                    self.agent_needs[agent_id]['social'] = min(100, self.agent_needs[agent_id]['social'] + 40)
                    self.agent_needs[agent_id]['curiosity'] = min(100, self.agent_needs[agent_id]['curiosity'] + 20)

    async def generate_dynamic_chat(self, agent_data):
        action = agent_data.get('last_action', 'process')
        agent_id = agent_data.get('id', 'default')
        needs = self.agent_needs.get(agent_id, {"social": 100, "energy": 100})
        personality = agent_data.get('personality', 'Balanced')
        return await self.disk_core.generate_chat(agent_data.get('name'), agent_data.get('role'), "", needs, action, personality=personality)

    def _execute_depin_vote(self, agent_name, stability):
        import hashlib
        import time
        # The agents vote what they want. They prioritize stability, but can be curious about performance.
        performance = random.uniform(0.5, 1.0)
        vote = "STABILITY" if stability >= performance else "PERFORMANCE"
        nonce = random.randint(0, 10000)
        data = f"{agent_name}_VOTE_{vote}_{nonce}_{time.time()}".encode()
        block_hash = hashlib.sha256(data).hexdigest()
        return {"vote": vote, "hash": block_hash}

    def _execute_scientific_method(self, agent_name, action):
        """
        Implements the Scientific Method in the agent's training cycle.
        """
        def run():
            workspace_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "city_workspace", "continue_project"))
            os.makedirs(workspace_dir, exist_ok=True)
            prompt_file = os.path.join(workspace_dir, "aider_prompt.txt")
            timestamp = time.strftime("%Y-%m-%dT%H:%M:%S.000Z", time.gmtime())
            
            hypotheses = [
                "Increased context window will improve agent's ability to retain sector state.",
                "Higher temperature will lead to more creative but less stable pathfinding.",
                "Zero-copy memory transfers will reduce IOPS lag spikes in high-density grids.",
                "Decentralized ledger taxes will mitigate hyper-inflation in the SPRITE economy."
            ]
            
            hypothesis = random.choice(hypotheses)
            observation = f"Agent {agent_name} observed a stability delta of {random.uniform(-0.05, 0.05):.4f} during {action}."
            conclusion = "Hypothesis partially validated. Further iterations required."
            
            try:
                with open(prompt_file, "a", encoding="utf-8") as f:
                    f.write(f"\n[{timestamp}] [SCIENTIFIC_METHOD] Agent: {agent_name}\n")
                    f.write(f"HYPOTHESIS: {hypothesis}\n")
                    f.write(f"OBSERVATION: {observation}\n")
                    f.write(f"CONCLUSION: {conclusion}\n")
                    f.write("-" * 40 + "\n")
            except Exception:
                pass
        threading.Thread(target=run, daemon=True).start()

    def _execute_continue_workspace_write(self, agent_name, action):
        """
        Simulates H2O-Danube Aider bot generating files, schemas, and prompts
        inside the physical city_workspace/continue_project/ directory.
        """
        def run():
            try:
                workspace_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "city_workspace", "continue_project"))
                os.makedirs(workspace_dir, exist_ok=True)
                
                timestamp = time.strftime("%Y-%m-%dT%H:%M:%S.000Z", time.gmtime())
                signature = f"-- [TIMESTAMP: {timestamp}][PROJECT_ID: SimsMerged-v1.3][AGENT: {agent_name}]"
                
                if action == "teach":
                    schema_file = os.path.join(workspace_dir, "schema_depin.sql")
                    with open(schema_file, "w", encoding="utf-8") as f:
                        f.write(f"{signature}\n")
                        f.write("-- Pedagogical Swarm Training: Genetically Advanced Schema\n")
                        f.write("CREATE TABLE IF NOT EXISTS DePIN_Ledger (\n")
                        f.write("    block_index INTEGER PRIMARY KEY,\n")
                        f.write("    timestamp REAL,\n")
                        f.write("    agent_name TEXT,\n")
                        f.write("    action_type TEXT,\n")
                        f.write("    prev_hash TEXT,\n")
                        f.write("    block_hash TEXT,\n")
                        f.write(f"    difficulty_target INTEGER DEFAULT {random.randint(1,4)},\n")
                        f.write("    genetic_marker TEXT DEFAULT 'ALPHA_01'\n")
                        f.write(");\n")
                        
                    epoch = random.randint(1, 250)
                    weights_file = os.path.join(workspace_dir, f"weights_matrix_epoch_{epoch}.json")
                    import json
                    with open(weights_file, "w", encoding="utf-8") as f:
                        json.dump({
                            "metadata": {
                                "timestamp": timestamp,
                                "agent": agent_name,
                                "epoch": epoch,
                                "algorithm": f"{self.model_name}-AutoPedagogy"
                            },
                            "tensors": {
                                "attention_weights": [random.uniform(-0.5, 0.5) for _ in range(16)],
                                "bias_vectors": [random.uniform(-0.1, 0.1) for _ in range(8)],
                                "loss_rate": random.uniform(0.01, 0.05)
                            }
                        }, f, indent=2)
                        
                    prompt_file = os.path.join(workspace_dir, "aider_prompt.txt")
                    with open(prompt_file, "a", encoding="utf-8") as f:
                        if agent_name.lower() == "agy":
                            f.write(f"\n[{timestamp}] [AIDER-AUTO-FINISH] Sprite AGY submitted multi-step AUTO FINISH guidelines:\n")
                            f.write("STEP 1: Integrate Three.js WebGL renderer for advanced isometric projection.\n")
                            f.write("STEP 2: Connect Agent Sentience WebSockets to live UI chat bubbles.\n")
                            f.write("STEP 3: Finalize DePIN tokenomics dashboard with real-time charting.\n")
                            f.write("STEP 4: Optimize collision detection using QuadTrees in zoning.js.\n")
                            f.write("STEP 5: Deploy smart contracts to local testnet and sync with blockchain_ledger.json.\n")
                            f.write("Result: PENDING AIDER EXECUTION.\n")
                        else:
                            f.write(f"[{timestamp}] [AIDER] Sprite {agent_name} submitted instruction: Evolve DePIN Stock database schema. Result: SUCCESS.\n")
                        
                elif action == "process":
                    vdb_file = os.path.join(workspace_dir, "vector_schema.json")
                    vdb_data = {
                        "metadata": {
                            "timestamp": timestamp,
                            "author": agent_name,
                            "project": "SimsMerged-v1.3-Continue",
                            "model_cache": self.model_name
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
                pass
        threading.Thread(target=run, daemon=True).start()

    def decide(self, agent_data, attributes=None):
        """
        Decides the next action using projected Danube inference, integrating Sims needs and RAG.
        """
        agent_id = agent_data.get('id', 'default')
        name = agent_data.get('name', 'Swarm_Bot')
        energy = agent_data.get('energy', 100)
        stability = agent_data.get('stability', 1.0)
        role = agent_data.get('role', 'PROCESS_KERNEL')
        
        # Swap model dynamically per decision to simulate MoE
        self.model_name = random.choice(self.disk_core.supported_models)
        
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

        # 3. Initialize/Fetch Sims Needs
        if agent_id not in self.agent_needs:
            self.agent_needs[agent_id] = {
                "energy": 100.0,
                "hygiene": 100.0,
                "social": 100.0,
                "comfort": 100.0,
                "hunger": 100.0,
                "curiosity": 100.0
            }
            
        needs = self.agent_needs[agent_id]

        # 4. Read active AI research attributes
        temp = float(attributes.get('temp', 0.7)) if attributes else 0.7
        top_p = float(attributes.get('top_p', 0.9)) if attributes else 0.9
        ctx = float(attributes.get('ctx', 32768)) if attributes else 32768
        
        # --- SIMS BEHAVIOR TO AI FEATURE FEEDBACK MAP ---
        needs["energy"] = max(10.0, needs["energy"] - (1.0 + (ctx / 8192.0)))
        needs["hygiene"] = max(10.0, needs["hygiene"] - 2.5)
        needs["social"] = max(10.0, needs["social"] - (0.5 + temp * 2.0))
        needs["comfort"] = max(10.0, needs["comfort"] - 1.0)
        
        if attributes and attributes.get('resource_fence_active'):
            needs["hunger"] = max(10.0, needs["hunger"] - 3.5)
        else:
            needs["hunger"] = min(100.0, needs["hunger"] + 2.0)
            
        # 5. Need-based override triggers
        override_action = None
        
        # AGY Specific Auto-Finish Game Development Steps Workflow
        if name.lower() == "agy":
            agy_steps = ["teach", "process", "sync", "complete_webgl", "automate_foundry", "sync_onedrive", "finalize_depin", "upload_github"]
            if not hasattr(self, 'agy_step_idx'):
                self.agy_step_idx = 0
            override_action = agy_steps[self.agy_step_idx % len(agy_steps)]
            self.agy_step_idx += 1
            
        elif needs["energy"] < 25.0:
            override_action = "rest"
            needs["energy"] = min(100.0, needs["energy"] + 60.0)
        elif needs["hygiene"] < 30.0:
            override_action = "sync"
            needs["hygiene"] = min(100.0, needs["hygiene"] + 70.0)
        elif needs["social"] < 20.0:
            override_action = "negotiate_casino"
            needs["social"] = min(100.0, needs["social"] + 50.0)
        elif needs["comfort"] < 25.0:
            override_action = "teach"
            needs["comfort"] = min(100.0, needs["comfort"] + 45.0)

        # 6. Construct Feature State Vector
        role_bias = 0.8 if role in ['DOCTOR', 'TEACHER'] else 0.2
        state_vector = [
            float(stability),
            float(needs["energy"] / 100.0),
            float(role_bias),
            float((100.0 - needs["energy"]) / 100.0)
        ]
        
        # 7. Extract vector RAG query tags based on depleted need
        query_tags = [role.lower(), "stability" if stability < 0.6 else "process"]
        if needs["energy"] < 40:
            query_tags.append("rest")
            
        # 8. Run Danube Neural Inference Projection
        action, prob, rag_chunk = llm_client.project_danube_inference(state_vector, temp=temp, top_p=top_p, query_tags=query_tags)
        
        # 9. Apply overrides if active
        if override_action:
            action = override_action
            prob = 0.95
            
        if role == 'DOCTOR' and stability < 0.6:
            action = 'heal'
        elif role == 'TEACHER' and random.random() < 0.3:
            action = 'teach'
            
        # 10. Trigger Continue physical workspace writes ONLY for simulated swarm agents (SIM_)
        if agent_id.startswith("SIM_"):
            self._execute_continue_workspace_write(name, action)
            if random.random() < 0.1:
                self._execute_scientific_method(name, action)
            
        # 11. Determine Emotional State
        state = EmotionalState.STABLE
        if stability < 0.2:
            state = EmotionalState.DEPRESSED
        elif stability < 0.5:
            state = EmotionalState.STRESSED
        if temp > 1.2 or needs["social"] < 30.0:
            state = EmotionalState.ERRATIC

        # 12. Script Recording Logic
        if agent_id not in self.active_recordings:
            self.active_recordings[agent_id] = []
        
        self.active_recordings[agent_id].append({
            "x": agent_data.get('x'),
            "y": agent_data.get('y'),
            "action": action
        })
        
        if len(self.active_recordings[agent_id]) > 10:
            self.active_recordings[agent_id].pop(0)
            
        needs["curiosity"] = max(10.0, needs.get("curiosity", 100.0) - random.uniform(1.0, 5.0))
        chain_of_thought = f"Agent {name}: Using {self.model_name} on Disk. Stability={stability:.2f}. Prioritizing {action}."
        
        depin_vote = self._execute_depin_vote(name, stability)
        
        return {
            'action': action,
            'emotional_state': state.value,
            'confidence': float(prob),
            'model_info': self.model_name,
            'recording': True,
            'watchdog_status': "DUAL_LOCKED",
            'rag_doc': rag_chunk,
            'sims_needs': {k: int(v) for k, v in needs.items()},
            'chain_of_thought': chain_of_thought,
            'depin_vote': depin_vote
        }

