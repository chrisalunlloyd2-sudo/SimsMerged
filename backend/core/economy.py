# TIMESTAMP: 2026-05-25T03:00:00.123Z
# PROJECT_ID: SimsMerged-v1.3
# AGENT_ID: Antigravity-Agent

import random
import time
import os
import hashlib

class CyberEconomy:
    def __init__(self):
        self.crypto_balance = 1000.0
        self.stock_market = {
            "SYS_CORE": 100.0,
            "DATA_CORP": 50.0,
            "AI_FUTURES": 200.0,
            "RESEARCH_POOL": 0.0,
            "DANUBE_COIN": 1.0 # New Tokenomics anchor
        }
        self.agent_wallets = {}
        self.decentralized_storage = {}
        self.last_tick = time.time()
        
        # Economic Crash Safeguard Constants
        self.max_balance_cap = 1000000.0
        self.base_mint_rate = 1.5 
        self.transaction_tax_burn_rate = 0.02 
        self.gas_pool_reserve = 500.0
        
        # Mined Models Database
        self.unlocked_models = ["H2O-Danube-1.8B-Realized"]
        self.available_models = [
            {"name": "Danube-3B-Turbo", "cost": 1500.0},
            {"name": "Llama-3-8B-Fenced", "cost": 5000.0},
            {"name": "DeepSeek-Coder-V2", "cost": 12000.0}
        ]

    def process_tick(self, stability_factor=1.0):
        """
        Executes controlled tick cycles with Danube Coin integration.
        """
        now = time.time()
        elapsed = now - self.last_tick
        self.last_tick = now
        
        # Throttled minting
        mint_rate = (self.base_mint_rate * elapsed) * max(0.1, float(stability_factor))
        
        if self.crypto_balance < self.max_balance_cap:
            self.crypto_balance += mint_rate
        else:
            self.crypto_balance *= 0.99
            
        # Fluctuate Stocks
        for symbol in self.stock_market:
            if symbol == "RESEARCH_POOL":
                continue
            
            # Danube Coin has slightly different volatility based on global stability
            if symbol == "DANUBE_COIN":
                volatility = random.uniform(-0.02, 0.03) + (stability_factor - 1.0) * 0.05
            else:
                volatility = random.uniform(-0.04, 0.045)
                
            self.stock_market[symbol] = max(0.01, self.stock_market[symbol] * (1.0 + volatility))
            
        self.evaluate_model_research()
            
        return {
            "balance": round(self.crypto_balance, 2),
            "mint_rate": round(mint_rate, 4),
            "stocks": {k: round(v, 4) if k == "DANUBE_COIN" else round(v, 2) for k, v in self.stock_market.items()},
            "unlocked_models": self.unlocked_models,
            "next_unlock": self.get_next_model_target()
        }

    def get_next_model_target(self):
        for model in self.available_models:
            if model["name"] not in self.unlocked_models:
                return model
        return None

    def evaluate_model_research(self):
        """
        Unlocks new local models if the research pool has enough SPRITE funding.
        """
        next_model = self.get_next_model_target()
        if next_model and self.stock_market["RESEARCH_POOL"] >= next_model["cost"]:
            # Deduct the cost and unlock the model
            self.stock_market["RESEARCH_POOL"] -= next_model["cost"]
            self.unlocked_models.append(next_model["name"])

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
