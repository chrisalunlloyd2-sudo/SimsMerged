import random

class ProgressionEngine:
    def __init__(self):
        self.global_level = 1
        self.agent_levels = {}
        self.titles = ['Novice', 'Adept', 'Expert', 'Master', 'Legend']

    def add_agent_xp(self, agent_name, xp):
        if agent_name not in self.agent_levels:
            self.agent_levels[agent_name] = {'level': 1, 'xp': 0, 'title': 'Novice'}
        
        self.agent_levels[agent_name]['xp'] += xp
        
        if self.agent_levels[agent_name]['xp'] >= 100:
            self.agent_levels[agent_name]['level'] += 1
            self.agent_levels[agent_name]['xp'] = 0
            self.global_level += 1
            return True
        return False

    def get_state(self):
        return {
            'global_level': self.global_level,
            'buffs': {'stability_recovery': 1.1}
        }
