import random

class CyberEconomy:
    def __init__(self):
        self.credits = 1000
        self.market_price = 100

    def process_tick(self):
        self.market_price = max(50, min(200, self.market_price + random.uniform(-5, 5)))
        self.credits = max(0, min(10000, self.credits + random.uniform(-50, 50)))
        return {'credits': self.credits, 'market_price': self.market_price}
