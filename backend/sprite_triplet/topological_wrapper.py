# TIMESTAMP: 2026-06-09
# PROJECT_ID: SimsMerged-v1.4.2
# AGENT_ID: viper_cli-architectssj4
# DESCRIPTION: Phase 6 - Topological Wrapping (Grid Fencing & Movement)

import os
import math
import logging
from typing import Tuple

logger = logging.getLogger("Topology")
logger.setLevel(logging.INFO)

class TopologicalGrid:
    def __init__(self, workspace_root: str = r"C:\Users\viper\Desktop\SimsMerged\WORKSPACE"):
        self.workspace_root = workspace_root
        if not os.path.exists(self.workspace_root):
            os.makedirs(self.workspace_root, exist_ok=True)

        # State memory for agent positions
        self.agent_positions = {}

    def assign_agent_coordinate(self, agent_id: str, x: int, y: int, z: int = 0):
        """Step 52: Assign agents (x,y,z) coordinates."""
        self.agent_positions[agent_id] = (x, y, z)

        # Step 53: Build filesystem mapper based on topology
        zone_dir = self._get_zone_path(x, y, z)
        if not os.path.exists(zone_dir):
            os.makedirs(zone_dir, exist_ok=True)

        logger.info(f"Agent {agent_id} bound to Topological Zone: ({x}, {y}, {z}) at {zone_dir}")

    def _get_zone_path(self, x: int, y: int, z: int) -> str:
        return os.path.join(self.workspace_root, f"ZONE_{x}_{y}_{z}")

    def calculate_travel_cost(self, agent_id: str, target_x: int, target_y: int, target_z: int = 0) -> float:
        """Step 59: Integrate topology with DePIN costs (distance = cost)."""
        if agent_id not in self.agent_positions:
            raise ValueError(f"Agent {agent_id} has no topological coordinate.")

        cur_x, cur_y, cur_z = self.agent_positions[agent_id]

        # Euclidean distance cost modifier
        distance = math.sqrt((target_x - cur_x)**2 + (target_y - cur_y)**2 + (target_z - cur_z)**2)

        # 1 unit of distance = 0.5 tokens
        cost = distance * 0.5
        logger.info(f"Travel cost from {cur_x},{cur_y},{cur_z} to {target_x},{target_y},{target_z} is {cost:.2f} tokens.")
        return cost

    def validate_write_permission(self, agent_id: str, target_file_path: str) -> bool:
        """Step 54 & 55: Restrict L3 writes to local topological zone."""
        if agent_id not in self.agent_positions:
            logger.error(f"Write Denied: Agent {agent_id} has no registered position.")
            return False

        x, y, z = self.agent_positions[agent_id]
        allowed_zone = self._get_zone_path(x, y, z)

        # Resolve target to absolute path
        abs_target = os.path.abspath(target_file_path)

        # Security Boundary Fencing Check (Step 60 prep)
        if not abs_target.startswith(allowed_zone):
            logger.warning(f"TOPOLOGY BREACH ATTEMPT: {agent_id} attempted write outside of Zone ({x},{y},{z}).")
            return False

        return True

    def cross_zone_read(self, requesting_agent: str, target_x: int, target_y: int, target_z: int, filename: str):
        """Step 56: Cross-zone file request API (Read-Only)."""
        target_dir = self._get_zone_path(target_x, target_y, target_z)
        target_path = os.path.join(target_dir, filename)

        if not os.path.exists(target_path):
            logger.info(f"Cross-zone read failed: {filename} not found in ({target_x},{target_y},{target_z}).")
            return None

        # Calculate DePIN cost for the read
        cost = self.calculate_travel_cost(requesting_agent, target_x, target_y, target_z)
        logger.info(f"Cross-zone read successful. Cost applied: {cost:.2f} tokens.")

        with open(target_path, "r", encoding="utf-8") as f:
            return f.read()

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    grid = TopologicalGrid()

    # Assign Agents
    grid.assign_agent_coordinate("L3_MINER", x=0, y=0)
    grid.assign_agent_coordinate("L3_BUILDER", x=5, y=5)

    # Validate boundary fence
    miner_zone = grid._get_zone_path(0, 0, 0)
    test_file = os.path.join(miner_zone, "mining_data.json")

    can_miner_write = grid.validate_write_permission("L3_MINER", test_file)
    print(f"Miner can write to its zone: {can_miner_write}")

    # Builder tries to write to Miner's zone (Should Fail)
    can_builder_write = grid.validate_write_permission("L3_BUILDER", test_file)
    print(f"Builder can write to Miner's zone: {can_builder_write}")

    # Calculate Travel Cost
    cost = grid.calculate_travel_cost("L3_MINER", target_x=5, target_y=5)
    print(f"Travel Cost Miner -> Builder: {cost:.2f} tokens")
