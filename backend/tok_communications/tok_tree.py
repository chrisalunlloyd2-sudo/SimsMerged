# TIMESTAMP: 2026-06-09
# PROJECT_ID: SimsMerged-v1.4.2
# AGENT_ID: viper_cli-architectssj4
# DESCRIPTION: Tok Tree with Backpressure Circuit Breaker

import uuid
import logging
from typing import Dict, List, Optional

logger = logging.getLogger("TokTree")
logger.setLevel(logging.INFO)

class TaskNode:
    def __init__(self, description: str, base_reward: float = 1.0):
        self.task_id = f"task_{uuid.uuid4().hex[:8]}"
        self.description = description
        self.status = "PENDING"  # PENDING, ASSIGNED, COMPLETED, FAILED
        self.assigned_agent: Optional[str] = None
        self.dependencies: List['TaskNode'] = []
        self.base_reward = base_reward

    def add_dependency(self, task: 'TaskNode'):
        self.dependencies.append(task)

    def can_execute(self) -> bool:
        return all(dep.status == "COMPLETED" for dep in self.dependencies)

class TokTreeDAG:
    def __init__(self):
        self.nodes: Dict[str, TaskNode] = {}
        self.agent_queues: Dict[str, int] = {} # agent_id -> queue_length

    def add_task(self, description: str, base_reward: float = 1.0) -> TaskNode:
        """Step 1 & 4: Define DAG for tasks & create funding logic based on complexity."""
        node = TaskNode(description, base_reward)
        self.nodes[node.task_id] = node
        logger.info(f"Task Added to Tok Tree: {node.task_id} | Reward: {base_reward} tokens")
        return node

    def link_dependency(self, parent_id: str, child_id: str):
        """Step 7: Build dependency resolution for tasks."""
        if parent_id in self.nodes and child_id in self.nodes:
            self.nodes[child_id].add_dependency(self.nodes[parent_id])
            logger.info(f"Linked Dependency: {child_id} depends on {parent_id}")

    def assign_task(self, task_id: str, agent_id: str) -> bool:
        """Step 6 / 23.3: Priority assignment with Backpressure Circuit Breaker."""
        if task_id not in self.nodes:
            return False
            
        # Step 23.3: Circuit Breaker Logic
        current_queue = self.agent_queues.get(agent_id, 0)
        if current_queue >= 10:
            logger.warning(f"CIRCUIT BREAKER: Agent {agent_id} queue too deep ({current_queue}). Halting assignment.")
            return False

        node = self.nodes[task_id]
        if not node.can_execute():
            logger.warning(f"Task {task_id} cannot be assigned. Dependencies not met.")
            return False
            
        node.status = "ASSIGNED"
        node.assigned_agent = agent_id
        
        # Update queue tracker
        self.agent_queues[agent_id] = current_queue + 1
        
        logger.info(f"Assigned {task_id} to Agent {agent_id}. Queue: {self.agent_queues[agent_id]}")
        return True

    def complete_task(self, task_id: str) -> float:
        """Completes task and releases reward."""
        if task_id in self.nodes:
            node = self.nodes[task_id]
            node.status = "COMPLETED"
            
            # Reduce queue length
            if node.assigned_agent in self.agent_queues:
                self.agent_queues[node.assigned_agent] = max(0, self.agent_queues[node.assigned_agent] - 1)
                
            logger.info(f"Task {task_id} completed. Releasing {node.base_reward} tokens.")
            return node.base_reward
        return 0.0

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    tree = TokTreeDAG()
    
    # Test Circuit Breaker
    agent = "L3_TEST_AGENT"
    for i in range(12):
        t = tree.add_task(f"Task {i}")
        tree.assign_task(t.task_id, agent)
