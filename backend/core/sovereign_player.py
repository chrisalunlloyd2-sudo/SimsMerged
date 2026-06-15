# [TIMESTAMP: 2026-06-14T19:00:00.000Z] [PROJECT_ID: SimsMerged-v1.4.2] [AGENT_ID: viper_cli-architectssj4]
# ACTION: Ascension Pillar V - Sovereign Player (Agentic Interaction)

import random
import asyncio
import json
import os
from .config import METROPOLIS_AGENTS, DISTRICTS, add_message, add_log

class SovereignPlayer:
    """
    Simulates agents 'playing' the game. 
    They move between nodes, interact with GUI components (virtually),
    and trigger the Data Syphon and EPMO loops.
    """
    def __init__(self):
        self.active = True

    async def simulate_movement(self, agent_id):
        # Virtually 'move' agent to a random district
        if not DISTRICTS: return
        district = random.choice(DISTRICTS)
        add_log(f"[SOVEREIGN_PLAYER] {agent_id} moved to {district['label']} ({district['type']})")
        
        # Interact based on district type
        if district['type'] == "RESEARCH_CENTER":
            add_message(agent_id, f"🧪 operating the Data Syphon at {district['label']}. Optimizing logic trees...")
        elif district['type'] == "REFRACTOR":
            add_message(agent_id, f"📡 Aligning neural beams at {district['label']} for 2x inference throughput.")
        elif district['type'] == "BUSINESS_SCHOOL":
            add_message(agent_id, f"🎓 Attending LSS seminar. Learning 'BM100' retrieval schemas.")

    async def agent_play_loop(self):
        add_log("🕹️ Sovereign Player active. Swarm is now playing the game and inventing patterns.")
        while self.active:
            # Pick a random agent to 'play'
            agent = random.choice(METROPOLIS_AGENTS)
            await self.simulate_movement(agent['id'])
            
            # Autonomous Invention Trigger (Sovereignty)
            if random.random() > 0.8: # 20% chance to attempt an invention
                concept = f"Auto_Optimization_{random.randint(100, 999)}"
                add_message(agent['id'], f"🧠 Sovereignty check: Attempting to invent '{concept}'.")
                
                # Mock generation of logic and test
                logic_stub = f"def optimize(): return 'Optimization for {concept} complete.'"
                test_stub = f"def test_optimize():\n    assert optimize() == 'Optimization for {concept} complete.'"
                
                try:
                    from backend.core.test_sovereignty import test_sovereignty
                    inv_id = await test_sovereignty.propose_invention(agent['id'], concept, logic_stub, test_stub)
                    await asyncio.sleep(2) # brief pause before execution
                    await test_sovereignty.execute_test(inv_id)
                except Exception as e:
                    add_log(f"[INVENTION_ERR] {e}", "error")

            # Genetic Swap / Joint Synthesis chance
            if random.random() > 0.85:
                agent2 = random.choice(METROPOLIS_AGENTS)
                if agent['id'] != agent2['id']:
                    # PHASE 25: JOINT SYNTHESIS HANDSHAKE
                    if random.random() > 0.5:
                        add_log(f"[CONSENSUS] Joint Synthesis initiated between {agent['name']} and {agent2['name']}.")
                        try:
                            from backend.main import joint_synthesis
                            project_name = f"Collaborative_Engine_{random.randint(100, 999)}"
                            asyncio.create_task(joint_synthesis(agent['id'], agent2['id'], project_name, "Build an advanced collaborative logic module."))
                        except: pass
                    else:
                        add_log(f"[GENETICS] Autonomous handshake triggered between {agent['name']} and {agent2['name']}.")
                        add_message(agent['id'], f"🧬 Initiating genetic handshake with {agent2['name']}. [AES-256 ACTIVE]")
                        
                        try:
                            from .evolution_council import evolution_council
                            asyncio.create_task(evolution_council.execute_genetic_handshake(agent['id'], agent2['id']))
                        except: pass
            
            await asyncio.sleep(random.randint(30, 90)) # Slow-burn interaction

sovereign_player = SovereignPlayer()

async def start_sovereign_play_loop():
    await sovereign_player.agent_play_loop()
