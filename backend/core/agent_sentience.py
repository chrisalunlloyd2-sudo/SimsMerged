import random

class SentienceEngine:
    def __init__(self):
        self.active_recordings = {}
        self.emotions = ['happy', 'neutral', 'stressed', 'learning']
        self.actions = ['process', 'heal', 'teach', 'negotiate_casino', 'heal_hospital']

    def decide(self, agent, attributes=None):
        action = random.choice(self.actions)
        confidence = random.uniform(0.6, 1.0)
        emotional_state = random.choice(self.emotions)
        
        decision = {
            'emotional_state': emotional_state,
            'action': action,
            'confidence': confidence,
            'model_info': 'Gemini-CLI-Architect v1.3',
            'watchdog_status': 'MONITORING',
            'recording': random.random() > 0.8,
            'script_id': None
        }
        
        if decision['recording']:
            self.active_recordings[agent.get('id', 'unknown')] = []
        
        return decision
