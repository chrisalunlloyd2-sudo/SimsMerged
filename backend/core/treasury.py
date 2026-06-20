# [TIMESTAMP: 2026-06-11T05:40:00.000Z] [PROJECT_ID: SimsMerged-v1.4.2] [AGENT_ID: Gemini-CLI-Architect]

import os
import json
import time
import hashlib
from typing import Dict, List, Optional
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from .config import SSD_SANDBOX_PATH, add_log, add_message

TREASURY_PATH = os.path.join(SSD_SANDBOX_PATH, "treasury_ledger.json")

class TreasurySystem:
    """
    PHASE 35: TREASURY POINT & DePIN ECONOMY
    - Manages 'Danube Coin' (DC) tokenomics.
    - Encrypted genetic data transfers (AES-256).
    - Behavioral rewards for 'Finish Line' success.
    """
    def __init__(self):
        self.ledger = self._load_ledger()
        self.encryption_key = os.urandom(32) # In-memory key for current session

    def _load_ledger(self) -> Dict:
        if os.path.exists(TREASURY_PATH):
            with open(TREASURY_PATH, "r") as f:
                return json.load(f)
        return {"balances": {}, "transactions": []}

    def _save_ledger(self):
        with open(TREASURY_PATH, "w") as f:
            json.dump(self.ledger, f, indent=2)

    def reward_agent(self, agent_id: str, amount: float, reason: str):
        """Rewards an agent for performance (e.g., successful synthesis)."""
        self.ledger["balances"][agent_id] = self.ledger["balances"].get(agent_id, 0) + amount
        self.ledger["transactions"].append({
            "time": time.time(),
            "agent_id": agent_id,
            "amount": amount,
            "reason": reason
        })
        self._save_ledger()
        add_log(f"[TREASURY] Rewarded {agent_id} with {amount} DC. Reason: {reason}")

    def get_balance(self, agent_id: str) -> float:
        return self.ledger["balances"].get(agent_id, 0.0)

    def secure_genetic_transfer(self, agent_id: str, data: Dict) -> str:
        """AES-256 CBC Encrypted genetic data transfer."""
        iv = os.urandom(16)
        cipher = Cipher(algorithms.AES(self.encryption_key), modes.CBC(iv), backend=default_backend())
        encryptor = cipher.encryptor()

        # Padding
        raw_data = json.dumps(data).encode()
        padding_len = 16 - (len(raw_data) % 16)
        raw_data += bytes([padding_len] * padding_len)

        ciphertext = encryptor.update(raw_data) + encryptor.finalize()

        # Record fee in treasury
        self.reward_agent(agent_id, -5.0, "Secure Genetic Transfer Fee")

        return (iv + ciphertext).hex()

treasury = TreasurySystem()
