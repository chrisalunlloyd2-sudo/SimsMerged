# TIMESTAMP: 2026-06-09
# PROJECT_ID: SimsMerged-v1.4.2
# AGENT_ID: viper_cli-architectssj4
# [PERFORMATIVE: ECONOMY_INVENTORY]
# DESCRIPTION: Phase 3.1 & 3.2 - Agent Inventory System & Gathering Logic

import sqlite3
import time
import asyncio
import logging
import os
import sys

# Ensure backend module is resolvable
sys.path.insert(0, r"C:\Users\viper\Desktop\SimsMerged")

from backend.sprite_triplet.depin_wallet import DePINLedger

logger = logging.getLogger("InventorySystem")
logger.setLevel(logging.INFO)

class InventorySystem:
    def __init__(self, db_path=r"C:\Users\viper\Desktop\SimsMerged\backend\inventory.db"):
        self.db_path = db_path
        self._init_db()
        self.ledger = DePINLedger()

    def _init_db(self):
        """Step 3.1: Create SQLite table schema for agent_inventory."""
        with sqlite3.connect(self.db_path) as conn:
            conn.execute('PRAGMA journal_mode=WAL;')
            cursor = conn.cursor()
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS agent_inventory (
                    agent_id TEXT,
                    item_id TEXT,
                    quantity INTEGER DEFAULT 0,
                    weight REAL DEFAULT 0.0,
                    PRIMARY KEY (agent_id, item_id)
                )
            ''')
            conn.commit()

    def add_item(self, agent_id, item_id, quantity=1, weight_per_unit=1.0):
        """Adds or updates an item in the agent's inventory."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO agent_inventory (agent_id, item_id, quantity, weight)
                VALUES (?, ?, ?, ?)
                ON CONFLICT(agent_id, item_id) DO UPDATE SET
                quantity = quantity + ?,
                weight = weight + ?
            ''', (agent_id, item_id, quantity, weight_per_unit * quantity, quantity, weight_per_unit * quantity))
            conn.commit()
        logger.info(f"Agent {agent_id} added {quantity} x {item_id} to inventory.")

    def get_inventory(self, agent_id):
        """Returns the full inventory for an agent."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT item_id, quantity, weight FROM agent_inventory WHERE agent_id = ?', (agent_id,))
            return cursor.fetchall()

    async def gather_resource(self, agent_id, terrain_type):
        """
        Step 3.2: Write the gather_resource logic.
        Agent at a specific tile spends 1 DePIN token and waits to add resource.
        """
        item_map = {
            0: ("Wood", 1.0, 1.5),  # Terrain 0 (Grass/Trees) -> Wood
            2: ("Stone", 1.0, 2.5)  # Terrain 2 (Stone) -> Stone
        }

        if terrain_type not in item_map:
            logger.warning(f"No gatherable resources at terrain type {terrain_type}.")
            return False

        item_id, cost, weight = item_map[terrain_type]

        # 1. Spend DePIN Token
        logger.info(f"Agent {agent_id} attempting to gather {item_id}. Cost: {cost} tokens.")
        if self.ledger.charge_inference_fee(agent_id, int(cost * 10000)): # abstract fee
            # 2. Wait 5 system "ticks" (simulated sleep)
            logger.info(f"Gathering {item_id} in progress (5 ticks)...")
            await asyncio.sleep(1.0) # 1 second simulated gathering time

            # 3. Add to inventory
            self.add_item(agent_id, item_id, 1, weight)
            return True
        else:
            logger.error(f"Gather failed: Agent {agent_id} has insufficient funds.")
            return False

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    inv = InventorySystem()

    # Test
    agent = "L3_PIONEER_01"
    # Ensure agent is funded for test
    inv.ledger.fund_wallet(agent, 10.0)

    import asyncio
    async def test():
        success = await inv.gather_resource(agent, 0)
        if success:
            items = inv.get_inventory(agent)
            print(f"Inventory: {items}")

    asyncio.run(test())
