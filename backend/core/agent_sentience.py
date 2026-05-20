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

    def decide(self, agent_data, attributes=None):
        """
        Decides the next action for an agent based on H2O-Danube optimization logic.
        """
        energy = agent_data.get('energy', 100)
        stability = agent_data.get('stability', 1.0)
        
        # 1. Dual-Watchdog Safety Check
        if not (self.watchdog_a_active and self.watchdog_b_active):
            return {
                'action': 'HALT', 
                'emotional_state': EmotionalState.UNSAFE.value, 
                'confidence': 0,
                'model_info': self.model_name,
                'clipboard_payload': "CRITICAL: Watchdog violation detected.",
                'watchdog_status': "BREACHED"
            }

        # 2. Determine Emotional State
        temp = float(attributes.get('temp', 0.7)) if attributes else 0.7
        top_p = float(attributes.get('top_p', 0.9)) if attributes else 0.9
        
        state = EmotionalState.STABLE
        if stability < 0.2: state = EmotionalState.DEPRESSED
        elif stability < 0.5: state = EmotionalState.STRESSED
        
        if temp > 1.2: state = EmotionalState.ERRATIC
        elif top_p > 0.95 and stability > 0.8: state = EmotionalState.CONFIDENT

        # 3. H2O-Danube Optimization Logic (Heal & Automate)
        action = 'process'
        if energy < 30: action = 'rest'
        elif stability < 0.6: action = 'sync' # Healing cycle
        else: action = 'move' # Autonomous exploration
        
        # 4. Automation Script Recording (Simulated)
        script_id = f"SCRIPT_{random.randint(100,999)}"
        
        return {
            'action': action,
            'emotional_state': state.value,
            'confidence': float(stability * 0.95),
            'model_info': self.model_name,
            'clipboard_payload': f"AGENT_SNAPSHOT: {agent_data.get('name')} | ACTION: {action} | SCRIPT: {script_id}",
            'watchdog_status': "DUAL_LOCKED"
        }
