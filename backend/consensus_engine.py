# TIMESTAMP: 2026-06-09
# PROJECT_ID: SimsMerged-v1.4.2
# AGENT_ID: viper_cli-architectssj4
# [PERFORMATIVE: CONSENSUS_ENGINE]
# DESCRIPTION: Chapter 14 - Multi-Stage Commit Protocol with Quadratic Voting & Ed25519 Signing

import asyncio
import json
import logging
import time
import httpx
import os
import sys
from typing import Dict, List, Set
from cryptography.hazmat.primitives.asymmetric import ed25519

# Ensure backend module is resolvable
sys.path.insert(0, r"C:\Users\viper\Desktop\SimsMerged")
from backend.sprite_triplet.depin_wallet import DePINLedger

logger = logging.getLogger("ConsensusEngine")
logger.setLevel(logging.INFO)

class ConsensusStage:
    PRE_PREPARE = "PRE-PREPARE"
    PREPARE = "PREPARE"
    COMMIT = "COMMIT"
    FINALIZED = "FINALIZED"

class ConsensusProtocol:
    def __init__(self, proposal_id: str, total_nodes: int):
        self.proposal_id = proposal_id
        self.total_nodes = total_nodes
        self.quorum = (2 * total_nodes // 3) + 1
        self.current_stage = ConsensusStage.PRE_PREPARE
        self.ledger = DePINLedger()

        self.votes = {
            ConsensusStage.PREPARE: set(),
            ConsensusStage.COMMIT: set()
        }
        self.start_time = time.time()

    async def advance_stage(self, stage: str, agent_id: str, chat_url: str):
        """Processes a vote for a specific stage."""
        if stage not in self.votes:
            return

        self.votes[stage].add(agent_id)
        count = len(self.votes[stage])

        logger.info(f"[CONSENSUS] {self.proposal_id} | Stage: {stage} | Votes: {count}/{self.quorum}")

        # Broadcast progress to GUI
        async with httpx.AsyncClient() as client:
            try:
                await client.post("http://127.0.0.1:8000/api/v1/agent/update", json={
                    "type": "CONSENSUS_UPDATE",
                    "proposal_id": self.proposal_id,
                    "stage": stage,
                    "vote_count": count,
                    "quorum": self.quorum
                })
            except: pass

        if count >= self.quorum:
            if self.current_stage == ConsensusStage.PRE_PREPARE and stage == ConsensusStage.PREPARE:
                self.current_stage = ConsensusStage.PREPARE
                logger.info(f"--- PROPOSAL {self.proposal_id} ADVANCED TO PREPARE ---")
            elif self.current_stage == ConsensusStage.PREPARE and stage == ConsensusStage.COMMIT:
                self.current_stage = ConsensusStage.COMMIT
                logger.info(f"--- PROPOSAL {self.proposal_id} ADVANCED TO COMMIT ---")

    async def cast_quadratic_vote(self, agent_id: str, vote_count: int, stage: str, chat_url: str, signature: str = None):
        """
        Step 14.2 & 14.3: Quadratic Voting with Ed25519 non-repudiation.
        Credit_Cost = (Allocated_Votes)^2
        """
        # Step 14.3: Signature Verification (Simulated)
        if signature is None:
            logger.warning(f"UNAUTHORIZED VOTE: Agent {agent_id} failed to provide cryptographic signature.")
            return False

        cost = float(vote_count ** 2)
        logger.info(f"Agent {agent_id} attempting to cast {vote_count} votes. Quadratic Cost: {cost}")

        # Charge the ledger
        if self.ledger._burn_tokens(agent_id, cost, "QUADRATIC_VOTE"):
            await self.advance_stage(stage, agent_id, chat_url)
            return True
        else:
            logger.warning(f"Vote rejected: {agent_id} has insufficient funds for quadratic cost.")
            return False

class SwarmConsensusManager:
    def __init__(self):
        self.active_proposals: Dict[str, ConsensusProtocol] = {}

    async def start_proposal(self, proposal_id: str, node_count: int):
        self.active_proposals[proposal_id] = ConsensusProtocol(proposal_id, node_count)
        logger.info(f"Consensus Initiated for {proposal_id}. Quorum required: {self.active_proposals[proposal_id].quorum}")

    async def cast_vote(self, proposal_id: str, agent_id: str, stage: str, vote_count: int = 1, signature: str = "ed25519_sim_sig"):
        if proposal_id in self.active_proposals:
            await self.active_proposals[proposal_id].cast_quadratic_vote(agent_id, vote_count, stage, "http://127.0.0.1:8000/api/v1/chat/send", signature)

            if self.active_proposals[proposal_id].current_stage == ConsensusStage.COMMIT:
                if len(self.active_proposals[proposal_id].votes[ConsensusStage.COMMIT]) >= self.active_proposals[proposal_id].quorum:
                    logger.info(f"🏆 CONSENSUS REACHED: {proposal_id} IS COMMITTED.")
                    self.active_proposals[proposal_id].current_stage = ConsensusStage.FINALIZED

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    manager = SwarmConsensusManager()

    async def simulate_quadratic_signed_bft():
        pid = "patch-signed-v1"
        await manager.start_proposal(pid, 3)

        # Fund Agents
        ledger = DePINLedger()
        ledger.fund_wallet("agent-1", 100.0)
        ledger.fund_wallet("agent-2", 100.0)
        ledger.fund_wallet("agent-3", 100.0)

        await manager.cast_vote(pid, "agent-1", ConsensusStage.PREPARE, vote_count=2, signature="sig_1")
        await manager.cast_vote(pid, "agent-2", ConsensusStage.PREPARE, vote_count=3, signature="sig_2")
        await manager.cast_vote(pid, "agent-3", ConsensusStage.PREPARE, vote_count=1, signature="sig_3")

        await manager.cast_vote(pid, "agent-1", ConsensusStage.COMMIT, vote_count=1, signature="sig_1")
        await manager.cast_vote(pid, "agent-2", ConsensusStage.COMMIT, vote_count=1, signature="sig_2")
        await manager.cast_vote(pid, "agent-3", ConsensusStage.COMMIT, vote_count=1, signature="sig_3")

    asyncio.run(simulate_quadratic_signed_bft())
