import random

class SystemIntegrity:
    def __init__(self):
        self.purge_count = 0
        self.current_weather = "CLEAR"
        self.weather_timer = 0
        self.weather_types = ["CLEAR", "DATA_RAIN", "CYBER_STORM", "ACID_CORRUPTION"]

    def process_weather(self):
        self.weather_timer += 1
        if self.weather_timer > 10:  # Faster weather shifts for visibility
            self.current_weather = random.choices(
                self.weather_types, 
                weights=[0.6, 0.2, 0.1, 0.1]
            )[0]
            self.weather_timer = 0
            
        weather_penalty = 0.0
        if self.current_weather == "DATA_RAIN":
            weather_penalty = 0.005
        elif self.current_weather == "CYBER_STORM":
            weather_penalty = 0.02
        elif self.current_weather == "ACID_CORRUPTION":
            weather_penalty = 0.05
            
        return weather_penalty

    def process_stability_net(self, current_stability, attributes=None):
        rag_k = float(attributes.get('rag_k', 10)) if attributes else 10
        mem_limit = float(attributes.get('mem', 24)) if attributes else 24
        
        weather_penalty = self.process_weather()
        
        recovery_rate = 0.005
        purge_threshold = 0.3
        
        recovery_multiplier = rag_k / 10.0
        applied_recovery = (recovery_rate * recovery_multiplier) - weather_penalty
        
        if mem_limit < 16:
            purge_threshold = 0.6
        elif mem_limit > 64:
            purge_threshold = 0.1
            
        should_purge = False
        if current_stability < purge_threshold:
            should_purge = True
            self.purge_count += 1
            
        return {
            'should_purge': should_purge,
            'recovery_increment': float(applied_recovery),
            'purge_threshold': float(purge_threshold),
            'status': 'AGGRESSIVE' if purge_threshold > 0.4 else 'STABLE',
            'weather': self.current_weather
        }

