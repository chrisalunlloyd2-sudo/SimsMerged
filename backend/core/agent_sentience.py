"""
[2026-05-17T17:50:45.120Z] [SimsMerged-v1.3-Metropolis] [Gemini-CLI-Architect]
AGENT SENTIENCE ENGINE - COGNITIVE DECISION LAYER
"""

class SentienceEngine:
    def __init__(self):
        print("[SentienceEngine] Cognitive Layer Online.")

    def decide(self, agent_data):
        """
        Takes agent energy/stability and returns a logical action.
        agent_data: dict containing 'energy' and 'stability'
        """
        energy = agent_data.get('energy', 100)
        stability = agent_data.get('stability', 1.0)

        if energy < 20:
            return "rest"
        elif stability < 0.5:
            return "calibrate"
        elif energy > 80:
            return "process"
        else:
            return "move"
