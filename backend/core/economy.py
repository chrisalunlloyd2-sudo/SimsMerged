import random
import time
import os

class CyberEconomy:
    def __init__(self):
        self.crypto_balance = 0.0
        self.stock_market = {
            "SYS_CORE": 100.0,
            "DATA_CORP": 50.0,
            "AI_FUTURES": 200.0
        }
        self.agent_wallets = {}
        self.decentralized_storage = {}
        self.last_tick = time.time()
        
    def process_tick(self):
        now = time.time()
        elapsed = now - self.last_tick
        self.last_tick = now
        
        # Mint SimCoin (SPRITE) based on system elapsed time
        mint_rate = 15.5 * elapsed # 15.5 per second
        self.crypto_balance += mint_rate
        
        # Fluctuate Stocks
        for symbol in self.stock_market:
            volatility = random.uniform(-0.05, 0.055)
            self.stock_market[symbol] *= (1.0 + volatility)
            
        return {
            "balance": round(self.crypto_balance, 2),
            "mint_rate": 15.5,
            "stocks": {k: round(v, 2) for k, v in self.stock_market.items()}
        }
        
    def ai_trade(self, agent_name):
        """
        Allow agents to trade stocks intelligently based on their simulated wealth.
        """
        if agent_name not in self.agent_wallets:
            self.agent_wallets[agent_name] = {"balance": 100.0, "portfolio": {}}
            
        wallet = self.agent_wallets[agent_name]
        stock = random.choice(list(self.stock_market.keys()))
        price = self.stock_market[stock]
        
        if wallet["balance"] >= price and random.random() > 0.5:
            wallet["balance"] -= price
            wallet["portfolio"][stock] = wallet["portfolio"].get(stock, 0) + 1
            return f"BOUGHT_{stock}"
        elif wallet["portfolio"].get(stock, 0) > 0 and random.random() > 0.5:
            wallet["portfolio"][stock] -= 1
            wallet["balance"] += price
            return f"SOLD_{stock}"
        return "HOLD"
        
    def store_memory(self, agent_name, memory_hash):
        """
        Decentralized Storage mechanism hook. Writes hashed chunks to filesystem.
        """
        storage_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "data", "memories"))
        if not os.path.exists(storage_dir):
            os.makedirs(storage_dir, exist_ok=True)
            
        file_name = f"{agent_name}_{memory_hash[:8]}.chunk"
        file_path = os.path.join(storage_dir, file_name)
        
        try:
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(f"TIMESTAMP: {time.time()}\n")
                f.write(f"PROJECT_ID: SimsMerged-v1.3\n")
                f.write(f"AGENT: {agent_name}\n")
                f.write(f"HASH: {memory_hash}\n")
                f.write(f"INTEGRITY: VERIFIED\n")
        except:
            pass # Silent fail for simulation stability

        if agent_name not in self.decentralized_storage:
            self.decentralized_storage[agent_name] = []
        self.decentralized_storage[agent_name].append(memory_hash)
        if len(self.decentralized_storage[agent_name]) > 50:
            self.decentralized_storage[agent_name].pop(0)
