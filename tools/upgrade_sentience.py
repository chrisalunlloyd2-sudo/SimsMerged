import os

sentience_path = r"C:\Users\viper\Desktop\SimsMerged\backend\core\agent_sentience.py"

new_code = """
import random
from enum import Enum

class EmotionalState(Enum):
    STABLE = "STABLE"
    STRESSED = "STRESSED"
    DEPRESSED = "DEPRESSED"
    CONFIDENT = "CONFIDENT"
    ERRATIC = "ERRATIC"

class SentienceEngine:
    def __init__(self):
        pass

    def decide(self, agent_data, attributes=None):
        \"\"\"
        Decides the next action for an agent based on energy, stability, and AI research attributes.
        \"\"\"
        energy = agent_data.get('energy', 100)
        stability = agent_data.get('stability', 1.0)

        # Default AI Attributes if none provided
        temp = float(attributes.get('temp', 0.7)) if attributes else 0.7
        top_p = float(attributes.get('top_p', 0.9)) if attributes else 0.9
        dropout = float(attributes.get('dropout', 0.2)) if attributes else 0.2

        # 1. Determine Emotional State
        state = EmotionalState.STABLE
        if stability < 0.2:
            state = EmotionalState.DEPRESSED
        elif stability < 0.5:
            state = EmotionalState.STRESSED

        # Impact of Temperature: High temp makes them erratic
        if temp > 1.2:
            state = EmotionalState.ERRATIC
        # Impact of Top-P: High top-p makes them confident
        elif top_p > 0.95 and stability > 0.8:
            state = EmotionalState.CONFIDENT

        # 2. Action Logic
        possible_actions = ['rest', 'process', 'move', 'sync']

        # Dropout impact: Randomly ignore 'best' choice
        if random.random() < dropout:
            action = random.choice(possible_actions)
        else:
            if state == EmotionalState.DEPRESSED:
                action = 'rest' # Only rest if depressed
            elif state == EmotionalState.ERRATIC:
                action = random.choice(possible_actions) # Pure randomness
            elif state == EmotionalState.CONFIDENT:
                action = 'process' # High-value processing
            else:
                action = 'move' if energy > 50 else 'rest'

        return {
            'action': action,
            'emotional_state': state.value,
            'confidence': top_p * stability
        }
"""

with open(sentience_path, "w", encoding="utf-8") as f:
    f.write(new_code)

print("Sentience Engine upgraded with research-driven behavioral logic!")
