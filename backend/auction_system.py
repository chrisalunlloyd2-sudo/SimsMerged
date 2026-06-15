# TIMESTAMP: 2026-06-09
# PROJECT_ID: SimsMerged-v1.4.2
# AGENT_ID: viper_cli-architectssj4
# DESCRIPTION: Phase 24.1 - Auction Engine (CNP Simulation)

import asyncio
import logging
import httpx
import sys
import os

# Ensure backend module is resolvable
sys.path.insert(0, r"C:\Users\viper\Desktop\SimsMerged")

from backend.agent_fsm import AgentFSM

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("AuctionEngine")

async def run_auction(task_name, task_type):
    logger.info(f"--- AUCTION START: {task_name} (Type: {task_type}) ---")
    
    # Simulate 3 competing agents with different capabilities
    agents = [
        AgentFSM("agent-math-expert", {"math": 0.9, "logic": 0.7}),
        AgentFSM("agent-extractor-v2", {"extraction": 0.8, "logic": 0.6}),
        AgentFSM("agent-general-worker", {"math": 0.4, "extraction": 0.4, "logic": 0.4})
    ]
    
    bids = []
    for agent in agents:
        cost = agent.calculate_bid(task_type)
        bids.append((agent.agent_id, cost))
        
    # Sort by lowest cost
    bids.sort(key=lambda x: x[1])
    winner_id, winner_cost = bids[0]
    
    logger.info(f"Auction Results: {bids}")
    logger.info(f"WINNER: {winner_id} with cost {winner_cost:.4f}")
    
    # Broadcast to GUI
    async with httpx.AsyncClient() as client:
        try:
            msg = f"[Auction] '{task_name}' awarded to {winner_id} (Cost: {winner_cost:.4f})"
            await client.post("http://127.0.0.1:8000/api/v1/chat/send", json={
                "sender_id": "AuctionBroker",
                "channel": "Economy",
                "message": msg
            })
            
            # Broadcast the details for each agent
            for aid, cost in bids:
                await client.post("http://127.0.0.1:8000/api/v1/chat/send", json={
                    "sender_id": aid,
                    "channel": "Economy",
                    "message": f"[BID] My computed cost for {task_type}: {cost:.4f}"
                })
                
        except Exception as e:
            logger.error(f"Failed to broadcast auction: {e}")

if __name__ == "__main__":
    asyncio.run(run_auction("Optimize Calculus Kernel", "math"))
