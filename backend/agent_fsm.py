# TIMESTAMP: 2026-06-09
# PROJECT_ID: SimsMerged-v1.4.2
# AGENT_ID: viper_cli-architectssj4
# [PERFORMATIVE: AGENT_FSM_AUCTION]
# DESCRIPTION: Phase 24.1 - Agent FSM with Hardware-Weighted Bidding

import time
import logging
import json
import psutil

logger = logging.getLogger("AgentFSM")
logger.setLevel(logging.INFO)

class AgentState:
    IDLE = "IDLE"
    PROCESSING = "PROCESSING"
    COMMUNICATING = "COMMUNICATING"
    COLLABORATING = "COLLABORATING"
    OPTIMIZING = "OPTIMIZING"

class AgentFSM:
    def __init__(self, agent_id, capability_matrix=None):
        self.agent_id = agent_id
        self.state = AgentState.IDLE
        self.funds = 10.0
        self.inventory = {}
        self.target_task = None
        self.home_coords = (0, 0)
        self.current_coords = (0, 0)

        # Step 10.3: Capability Matrix (Skills Vector)
        # Default: normalized weights for different domains
        self.capabilities = capability_matrix or {
            "math": 0.5,
            "extraction": 0.5,
            "logic": 0.5,
            "social": 0.5
        }

    def calculate_bid(self, task_type: str) -> float:
        """
        Step 24.1: Hardware-Weighted Bidding Formula.
        Cost = w1 * CPU + w2 * Mem + w3 * (1 - Cap)
        Lower cost wins.
        """
        # Weights (Hyperparameters for swarm balance)
        w1, w2, w3 = 0.3, 0.2, 0.5

        cpu_load = psutil.cpu_percent() / 100.0
        mem_util = psutil.virtual_memory().percent / 100.0
        capability_score = self.capabilities.get(task_type.lower(), 0.5)

        cost = (w1 * cpu_load) + (w2 * mem_util) + (w3 * (1.0 - capability_score))

        logger.info(f"Agent {self.agent_id} calculated bid cost for {task_type}: {cost:.4f}")
        return cost

    def update(self):
        """Industrial 5-State model."""
        if self.funds <= 0 and any(self.inventory.values()):
            self.state = AgentState.COMMUNICATING
            return self.state

        if self.state == AgentState.IDLE:
            if self.target_task:
                self.state = AgentState.PROCESSING
                logger.info(f"Agent {self.agent_id} -> PROCESSING task {self.target_task}")

        elif self.state == AgentState.PROCESSING:
            self.state = AgentState.COLLABORATING

        elif self.state == AgentState.COLLABORATING:
            self.state = AgentState.OPTIMIZING

        elif self.state == AgentState.OPTIMIZING:
            logger.info(f"Agent {self.agent_id} finished self-optimization.")
            self.state = AgentState.IDLE
            self.target_task = None

        return self.state

    def to_json(self):
        return {
            "type": "AGENT_UPDATE",
            "agent_id": self.agent_id,
            "x": self.current_coords[0],
            "y": self.current_coords[1],
            "status": self.state,
            "funds": self.funds,
            "inventory": self.inventory,
            "capabilities": self.capabilities
        }

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    test_agent = AgentFSM("AUCTION_BOT_01", {"math": 0.9, "logic": 0.8})
    bid = test_agent.calculate_bid("math")
    print(f"Final Bid Cost: {bid:.4f}")
