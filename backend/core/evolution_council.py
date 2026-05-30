# TIMESTAMP: 2026-05-30T00:37:00.000Z
# PROJECT_ID: SimsMerged-v1.3-Metropolis
# AGENT_ID: Antigravity-Agent

import asyncio
import time
import os
import random
import json
import subprocess
import hashlib
from backend.core.neuromorphic_core import neuromorphic_core

class EvolutionCouncil:
    def __init__(self):
        self.interval_seconds = 3600 # Once an hour
        self.workspace_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "city_workspace", "continue_project"))
        os.makedirs(self.workspace_dir, exist_ok=True)
        self.models = ["Triton-Danube-1.8B", "Triton-Smoll-0.5B", "Triton-Qwen-1.5B"]

    async def execute_web_crawl(self):
        """Simulates injecting web crawls and mini-projects for them to learn about AI and programming."""
        print("[EVOLUTION_COUNCIL] Initiating neuromorphic web crawl...")
        
        # Neuromorphic Intent Parsing for crawl direction
        hash_val, gate = neuromorphic_core.parse_intent("LEARN ADVANCED PROGRAMMING AI SCHEMAS")
        
        # Curated Pedagogical Curriculum Topics
        topics = [
            "Advanced Graph RAG Schemas",
            "Zero-copy InfiniBand Networking",
            "Rust-based Node Auto-Scaling",
            "DePIN Crypto Tokenomics via Smart Contracts",
            "Isometric WebGL rendering optimization",
            "Generative AI Agent Chat prompt engineering",
            "Dynamic Urban Zoning Algorithms",
            "A* Pathfinding for Swarm Agents",
            "Procedural Building Asset Generation",
            "Low-latency Packet Interconnects",
            "Headless UI Vision & Automated Grading",
            "AES-256 Genetic Data Encryption",
            "DePIN Stock Market Volatility Heuristics"
        ]
        chosen_topic = random.choice(topics)
        await asyncio.sleep(2) 
        
        return {
            "topic": chosen_topic,
            "hash": hash_val,
            "complexity": random.randint(1, 10),
            "schema_prototype": f"CREATE TABLE IF NOT EXISTS {chosen_topic.replace(' ', '_')} (id INT, data TEXT);"
        }

    async def trigger_manual_vote(self):
        """Forces an immediate web-crawl and voting sequence."""
        crawl_data = await self.execute_web_crawl()
        approved = await self.execute_vote(crawl_data)
        if approved:
            await self.apply_mini_project(crawl_data)
            await self.push_to_github(crawl_data)
        return approved

    async def execute_vote(self, crawl_data, agents_list=None):
        """
        Ecosystem simulated agents vote on whether to integrate the mini-project.
        Dynamic, role-based reasoning is evaluated and posted live to the MSN chat interface.
        """
        print(f"[EVOLUTION_COUNCIL] Swarm agents voting on mini-project: {crawl_data['topic']}")
        
        # Update global state for UI tracking
        from backend import main
        main.CURRENT_EVOLUTION_PROJECT = {
            "topic": crawl_data['topic'],
            "status": "VOTING_IN_PROGRESS",
            "hash": crawl_data['hash']
        }
        
        # MSN CHAT: Inject council announcement
        main.add_message("Evolution_Council", f"🔊 [ANNOUNCEMENT] Proposed Integration: '{crawl_data['topic']}'. Swarm voting sequence initiated.", crawl_data['hash'])
        await asyncio.sleep(1.5)

        # Get active simulated agents
        agents = main.SIMULATED_AGENTS
        if not agents or len(agents) == 0:
            # Fallback to simulated swarm roles if no active agents are spawned
            agents = [
                {"id": "SIM_DOCTOR_88", "name": "Sprite_Doctor_88", "role": "DOCTOR", "stability": 0.85},
                {"id": "SIM_TEACHER_12", "name": "Sprite_Teacher_12", "role": "TEACHER", "stability": 0.90},
                {"id": "SIM_KERNEL_44", "name": "Sprite_Kernel_44", "role": "PROCESS_KERNEL", "stability": 0.95}
            ]
            
        votes = []
        approvals = 0
        rejections = 0
        topic_lower = crawl_data['topic'].lower()
        complexity = crawl_data.get('complexity', random.randint(1, 10))

        for agent in agents:
            name = agent.get("name", "Swarm_Bot")
            role = agent.get("role", "PROCESS_KERNEL")
            agent_id = agent.get("id", "default")
            
            # Retrieve agent's needs from SentienceEngine
            needs = main.sentience_engine.agent_needs.get(agent_id, {"energy": 100, "social": 100})
            energy = needs.get("energy", 100)
            
            vote = "APPROVE"
            reason = "A robust addition to our system schema."

            if energy < 35:
                vote = "REJECT"
                reason = "Simulation load is too high. My core energy is depleted."
            elif role == "DOCTOR":
                if "stability" in topic_lower or "ecc" in topic_lower or "healing" in topic_lower or "cooling" in topic_lower or "zero-copy" in topic_lower or "protection" in topic_lower:
                    vote = "APPROVE"
                    reason = "Directly improves our system reliability and thermal metrics."
                elif complexity > 7:
                    vote = "REJECT"
                    reason = f"Integration complexity is too high ({complexity}/10). Risks core instability!"
                else:
                    vote = random.choice(["APPROVE", "REJECT"])
                    reason = "Meets nominal core metrics." if vote == "APPROVE" else "Core integrity must take priority over new files."
            elif role == "TEACHER":
                if "rag" in topic_lower or "ai" in topic_lower or "neural" in topic_lower or "learning" in topic_lower or "prompt" in topic_lower or "weight" in topic_lower:
                    vote = "APPROVE"
                    reason = "Directly strengthens our soft-prompt tuning and neural matrices!"
                else:
                    vote = "APPROVE"
                    reason = "Education schemas and knowledge sharing are always optimal."
            elif role == "PROCESS_KERNEL":
                if "speed" in topic_lower or "packet" in topic_lower or "network" in topic_lower or "latency" in topic_lower or "zero-copy" in topic_lower or "nvme" in topic_lower or "thread" in topic_lower or "iops" in topic_lower:
                    vote = "APPROVE"
                    reason = "Optimizes priority thread scheduling and zero-copy transfer routes."
                elif "crypto" in topic_lower or "depin" in topic_lower or "token" in topic_lower or "ledger" in topic_lower:
                    vote = "APPROVE"
                    reason = "Increases block difficulty mining rates and DePIN token rewards."
                else:
                    vote = random.choice(["APPROVE", "REJECT"])
                    reason = "Fits within our thread allocation parameters." if vote == "APPROVE" else "High risk of context switching overhead."

            votes.append((name, vote))
            if vote == "APPROVE":
                approvals += 1
            else:
                rejections += 1
                
            # Post dynamic reasoning live into MSN Chat with color indicators
            indicator = "🟩 APPROVE" if vote == "APPROVE" else "🟥 REJECT"
            main.add_message(name, f"[{indicator}] \"{reason}\"", crawl_data['hash'])
            await asyncio.sleep(0.5) # Dramatic pause between votes

        total_votes = len(votes)
        passed = approvals > (total_votes / 2)
        result = "PASSED" if passed else "REJECTED"
        
        main.CURRENT_EVOLUTION_PROJECT["status"] = result
        main.add_message("Evolution_Council", f"📊 [VOTE RESULT] The proposed module '{crawl_data['topic']}' has {result}! (Tally: {approvals} approvals, {rejections} rejections).", crawl_data['hash'])
        
        if result == "PASSED":
            # SIGNAL AGY: This actually builds the game by updating engine.js
            await self.ship_to_agy(crawl_data)
            
        return result == "PASSED"

    async def ship_to_agy(self, crawl_data):
        """Builds the game by injecting new capabilities into engine.js (AGY Integration)"""
        print(f"[EVOLUTION_COUNCIL] Shipping {crawl_data['topic']} to AGY (Frontend Engine)...")
        
        engine_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "frontend", "js", "engine.js"))
        if os.path.exists(engine_path):
            try:
                # Procedural building type generation based on topic
                type_id = crawl_data['topic'].replace(' ', '_').upper()[:10]
                new_build_type = f"""
    '{type_id}': {{ 
        color: '#{hashlib.md5(type_id.encode()).hexdigest()[:6]}', 
        label: '{crawl_data['topic']}', 
        locked: false, 
        category: 'Evolution', 
        desc: 'Genetically advanced {crawl_data['topic']} node.' 
    }},"""
                
                with open(engine_path, "r", encoding="utf-8") as f:
                    content = f.read()
                
                if "const BUILD_TYPES = {" in content:
                    content = content.replace("const BUILD_TYPES = {", f"const BUILD_TYPES = {{{new_build_type}")
                    with open(engine_path, "w", encoding="utf-8") as f:
                        f.write(content)
                
                from backend import main
                main.add_log(f"AGY_SHIPMENT: Successfully integrated {type_id} into Metropolis Engine JS.", "info")
            except Exception as e:
                print(f"[EVOLUTION_COUNCIL_ERROR] Failed to ship to AGY: {e}")

    async def apply_mini_project(self, crawl_data):
        """Applies the schema and programmatic capability additively (NEVER DELETE)"""
        timestamp = time.strftime("%Y%m%d_%H%M%S")
        
        # 1. Generate Backend Schema
        sql_filename = f"mini_project_{timestamp}.sql"
        sql_filepath = os.path.join(self.workspace_dir, sql_filename)
        with open(sql_filepath, "w", encoding="utf-8") as f:
            f.write(f"-- [GENETIC ADVANCEMENT] Topic: {crawl_data['topic']}\n")
            f.write(f"-- Models used: {', '.join(self.models)} (Disk Cache)\n")
            f.write(crawl_data["schema_prototype"] + "\n")
            
        print(f"[EVOLUTION_COUNCIL] Applied additive backend schema: {sql_filename}")

    async def push_to_github(self, crawl_data):
        """Updates to GitHub ensuring we NEVER DELETE ANYTHING (Additive commits)"""
        print("[EVOLUTION_COUNCIL] Pushing evolutionary genetic traits to GitHub...")
        try:
            # Call the existing github sync script
            sync_script = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "github", "github_sync.ps1"))
            if os.path.exists(sync_script):
                cmd = f'powershell.exe -NoProfile -ExecutionPolicy Bypass -Command "& \'{sync_script}\' -CommitMessage \'Evolution Council: Genetically advanced schema for {crawl_data["topic"]}\'"'
                subprocess.Popen(cmd, shell=True)
                print("[EVOLUTION_COUNCIL] GitHub Sync initiated in background.")
            else:
                print("[EVOLUTION_COUNCIL] GitHub sync script not found, skipping push.")
        except Exception as e:
            print(f"[EVOLUTION_COUNCIL] Failed to push to GitHub: {e}")

    async def start_evolution_loop(self):
        print("[EVOLUTION_COUNCIL] Online. Hourly voting and web-crawling active.")
        # Do a quick initial run after 30 seconds to kickstart it, then hourly.
        await asyncio.sleep(30)
        
        while True:
            try:
                crawl_data = await self.execute_web_crawl()
                approved = await self.execute_vote(crawl_data)
                
                if approved:
                    await self.apply_mini_project(crawl_data)
                    await self.push_to_github(crawl_data)
                else:
                    print("[EVOLUTION_COUNCIL] Mini-project rejected by consensus. Evolving communication instead.")
                    
            except Exception as e:
                print(f"[EVOLUTION_COUNCIL_ERROR] {e}")
                
            print(f"[EVOLUTION_COUNCIL] Hibernating for 1 hour. SLOWLY building the environment.")
            await asyncio.sleep(self.interval_seconds)

evolution_council = EvolutionCouncil()
