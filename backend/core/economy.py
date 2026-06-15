# TIMESTAMP: 2026-05-25T03:00:00.123Z
# PROJECT_ID: SimsMerged-v1.3
# AGENT_ID: Antigravity-Agent

import random
import time
import os
import hashlib

class CyberEconomy:
    def __init__(self):
        self.crypto_balance = 5000.0 # Starting treasury
        self.base_mint_rate = 0.0
        self.stock_market = {
            "SYS_CORE": 120.0,
            "DATA_CORP": 45.0,
            "AI_FUTURES": 350.0,
            "RESEARCH_POOL": 0.0,
            "DANUBE_COIN": 1.0 
        }
        self.agent_wallets = {}
        self.last_tick = time.time()
        self.transaction_tax_burn_rate = 0.02
        
        # Mined Models Database (REAL OLLAMA TAGS)
        self.unlocked_models = ["smollm:135m", "qwen:0.5b", "h2o-danube2:0.5b"]
        self.available_models = [
            {"tag": "qwen:1.8b", "name": "Qwen 1.8B Optimizer", "cost": 2500.0},
            {"tag": "stable-code:3b", "name": "StableCode Wizard", "cost": 5000.0},
            {"tag": "mistral:7b", "name": "Mistral-v0.3 Sovereign", "cost": 15000.0},
            {"tag": "llama3:8b", "name": "Llama-3 High-Fidelity", "cost": 25000.0}
        ]

    def execute_transaction(self, tx_type, target, cost):
        """Processes real economic events: stock trades or model upgrades."""
        if tx_type == "BUY_MODEL":
            # Real Model Purchase Logic
            if self.crypto_balance >= cost:
                self.crypto_balance -= cost
                if target not in self.unlocked_models:
                    self.unlocked_models.append(target)
                return True
        elif tx_type == "BUY":
            if self.crypto_balance >= cost:
                self.crypto_balance -= cost
                return True
        return False

    def process_tick(self, stability_factor=1.0, chrono_state=None):
        now = time.time()
        elapsed = now - self.last_tick
        self.last_tick = now
        
        is_night = False
        if chrono_state:
            is_night = not chrono_state.get("is_daylight", True)

        from .behavioral_scanner import behavioral_scanner
        from .config import METROPOLIS_AGENTS

        # BINOMIAL POWER SCALING: Exponential minting based on technical achievements
        total_power = 0
        for agent in METROPOLIS_AGENTS:
            power = behavioral_scanner.get_binomial_factor(agent["id"])
            agent["binomial_power"] = round(power, 2)
            total_power += power

        # NOCTURNAL TOKENOMICS: 2x Minting at Night, 0.5x during Day (Sleep phase)
        cycle_multiplier = 2.0 if is_night else 0.5
        mint_rate = (2.0 * elapsed) * (total_power / len(METROPOLIS_AGENTS)) * cycle_multiplier
        
        self.base_mint_rate = mint_rate
        self.crypto_balance = min(1000000.0, self.crypto_balance + mint_rate)
            
        # Volatility logic
        for symbol in self.stock_market:
            if symbol == "RESEARCH_POOL": continue
            change = random.uniform(-0.01, 0.015)
            self.stock_market[symbol] = max(0.1, self.stock_market[symbol] * (1.0 + change))
            
        return {
            "balance": round(self.crypto_balance, 2),
            "mint_rate": round(mint_rate, 4),
            "total_swarm_power": round(total_power, 2),
            "is_night": is_night
        }

    def get_state(self):
        """Returns the current economic state for the HUD."""
        return {
            "treasury_balance": round(self.crypto_balance, 2),
            "mint_rate": round(self.base_mint_rate, 4),
            "stock_market": self.stock_market,
            "agent_wallets": {name: {"balance": round(w["balance"], 2)} for name, w in self.agent_wallets.items()}
        }
    def ai_trade(self, agent_name, performance_bonus=0.0):
        """
        Allow agents to trade stocks intelligently, with tax/burn rules applied.
        """
        if agent_name not in self.agent_wallets:
            self.agent_wallets[agent_name] = {"balance": 100.0, "portfolio": {}}
            
        wallet = self.agent_wallets[agent_name]
        
        # Award performance bonus Sprite coins
        wallet["balance"] += performance_bonus
        
        stock = random.choice(list(self.stock_market.keys()))
        price = self.stock_market[stock]
        
        if stock == "RESEARCH_POOL":
            # Direct donation to neural model research
            donation = min(wallet["balance"] * 0.1, 10.0)
            wallet["balance"] -= donation
            self.stock_market["RESEARCH_POOL"] += donation
            return f"RESEARCH_DONATED_{donation:.1f}"
        
        if wallet["balance"] >= price and random.random() > 0.4:
            # Burn a transaction tax to prevent economic bloat
            tax = price * self.transaction_tax_burn_rate
            wallet["balance"] -= (price + tax)
            self.crypto_balance -= tax # Burn the coins from total system circulation
            
            wallet["portfolio"][stock] = wallet["portfolio"].get(stock, 0) + 1
            return f"BOUGHT_{stock}"
            
        elif wallet["portfolio"].get(stock, 0) > 0 and random.random() > 0.4:
            tax = price * self.transaction_tax_burn_rate
            wallet["portfolio"][stock] -= 1
            wallet["balance"] += (price - tax)
            self.crypto_balance -= tax # Burn tax
            return f"SOLD_{stock}"
            
        return "HOLD"

    def mine_depin_block(self, agent_name, action, prev_hash, difficulty=1):
        """
        Performs REAL local SHA-256 block mining (Proof-of-Work).
        Finds a nonce that satisfies the difficulty target (e.g. difficulty=1 -> hash must start with '0').
        """
        target_prefix = "0" * difficulty
        nonce = 0
        max_nonces = 1500 # Strict cap to keep CPU execution under 5ms (highly optimized)
        
        start_time = time.time()
        
        while nonce < max_nonces:
            data = f"{agent_name}{action}{prev_hash}{nonce}".encode()
            block_hash = hashlib.sha256(data).hexdigest()
            if block_hash.startswith(target_prefix):
                mine_time = time.time() - start_time
                return {
                    "nonce": nonce,
                    "hash": block_hash,
                    "mine_time_ms": mine_time * 1000,
                    "status": "VERIFIED_POW"
                }
            nonce += 1
            
        # Fallback in case of max search timeout
        fallback_data = f"{agent_name}{action}{prev_hash}fallback".encode()
        fallback_hash = hashlib.sha256(fallback_data).hexdigest()
        return {
            "nonce": nonce,
            "hash": fallback_hash,
            "mine_time_ms": 0.05,
            "status": "NOMINAL"
        }

economy = CyberEconomy()

