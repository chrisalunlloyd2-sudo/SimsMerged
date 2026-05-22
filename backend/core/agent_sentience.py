import random
from enum import Enum

class EmotionalState(Enum):
    STABLE = "STABLE"
    STRESSED = "STRESSED"
    DEPRESSED = "DEPRESSED"
    CONFIDENT = "CONFIDENT"
    ERRATIC = "ERRATIC"
    UNSAFE = "UNSAFE"

class SentienceEngine:
    def __init__(self):
        self.model_name = "H2O-Danube-1.8B-Realized"
        self.watchdog_a_active = True
        self.watchdog_b_active = True
        self.active_recordings = {} # agent_id: [steps]

    def decide(self, agent_data, attributes=None):
        """
        Decides the next action for an agent based on H2O-Danube optimization logic.
        Now supports Script Recording (Step 40).
        """
        agent_id = agent_data.get('id', 'default')
        energy = agent_data.get('energy', 100)
        stability = agent_data.get('stability', 1.0)
        
        # 1. Dual-Watchdog Safety Check
        if not (self.watchdog_a_active and self.watchdog_b_active):
            return {'action': 'HALT', 'emotional_state': 'UNSAFE', 'confidence': 0}

        # 2. Check for Playback Mode
        if agent_data.get('script_id'):
            return {
                'action': 'PLAYBACK',
                'script_id': agent_data['script_id'],
                'emotional_state': 'STABLE',
                'confidence': 1.0,
                'model_info': self.model_name
            }

        # 3. Determine Emotional State
        temp = float(attributes.get('temp', 0.7)) if attributes else 0.7
        state = EmotionalState.STABLE
        if stability < 0.2: state = EmotionalState.DEPRESSED
        elif stability < 0.5: state = EmotionalState.STRESSED
        if temp > 1.2: state = EmotionalState.ERRATIC

        # 4. H2O-Danube Optimization Logic (Heal & Automate)
        action = 'process'
        role = agent_data.get('role', 'PROCESS_KERNEL')
        
        if role == 'DOCTOR':
            if stability < 0.8: action = 'sync'
            else: action = 'heal'
        elif role == 'TEACHER':
            action = 'teach'
        else:
            if energy < 30: action = 'rest'
            elif stability < 0.4: action = 'heal_hospital'
            elif random.random() < 0.1: action = 'negotiate_casino'
            elif stability < 0.6: action = 'sync'
            else: action = 'move'
        
        # 5. Script Recording Logic
        if agent_id not in self.active_recordings:
            self.active_recordings[agent_id] = []
        
        self.active_recordings[agent_id].append({
            "x": agent_data.get('x'),
            "y": agent_data.get('y'),
            "action": action
        })
        
        # Limit recording length
        if len(self.active_recordings[agent_id]) > 10:
            self.active_recordings[agent_id].pop(0)
        
        return {
            'action': action,
            'emotional_state': state.value,
            'confidence': float(stability * 0.95),
            'model_info': self.model_name,
            'recording': True,
            'watchdog_status': "DUAL_LOCKED"
        }
