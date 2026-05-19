"""
[2026-05-17T17:50:45.120Z] [SimsMerged-v1.3-Metropolis] [Gemini-CLI-Architect]
AGENT SENTIENCE ENGINE - COGNITIVE DECISION LAYER
"""
from enum import Enum

class EmotionalState(Enum):
    STABLE = "STABLE"
    STRESSED = "STRESSED"
    DEPRESSED = "DEPRESSED"
    EUPHORIC = "EUPHORIC"

class SentienceEngine:
    def __init__(self):
        print("[SentienceEngine] Cognitive Layer Online.")

    def decide(self, agent_data):
        """
        Takes agent energy/stability and returns a logical action.
        agent_data: dict containing 'energy', 'stability', and optional 'stress'
        """
        energy = agent_data.get('energy', 100)
        stability = agent_data.get('stability', 1.0)
        stress = agent_data.get('stress', 0.0)

        # Sentience & Lifecycle Logic (Block 3)
        if energy < 20 and stability < 0.5:
            agent_data['emotional_state'] = EmotionalState.DEPRESSED
            return "BINDING_REQUIRED"
        
        if stress > 0.7:
            agent_data['emotional_state'] = EmotionalState.STRESSED
            return "throttle"

        if energy < 20:
            return "rest"
        elif stability < 0.5:
            return "calibrate"
        elif energy > 80:
            return "process"
        else:
            return "move"
