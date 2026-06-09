$sentience_path = "C:\Users\viper\Desktop\SimsMerged\backend\core\agent_sentience.py"
$new_code = @"
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
        energy = agent_data.get('energy', 100)
        stability = agent_data.get('stability', 1.0)
        
        temp = float(attributes.get('temp', 0.7)) if attributes else 0.7
        top_p = float(attributes.get('top_p', 0.9)) if attributes else 0.9
        dropout = float(attributes.get('dropout', 0.2)) if attributes else 0.2

        state = EmotionalState.STABLE
        if stability < 0.2:
            state = EmotionalState.DEPRESSED
        elif stability < 0.5:
            state = EmotionalState.STRESSED
            
        if temp > 1.2:
            state = EmotionalState.ERRATIC
        elif top_p > 0.95 and stability > 0.8:
            state = EmotionalState.CONFIDENT

        possible_actions = ['rest', 'process', 'move', 'sync']
        
        if random.random() < dropout:
            action = random.choice(possible_actions)
        else:
            if state == EmotionalState.DEPRESSED:
                action = 'rest'
            elif state == EmotionalState.ERRATIC:
                action = random.choice(possible_actions)
            elif state == EmotionalState.CONFIDENT:
                action = 'process'
            else:
                action = 'move' if energy > 50 else 'rest'

        return {
            'action': action,
            'emotional_state': state.value,
            'confidence': float(top_p * stability)
        }
"@
Set-Content -Path $sentience_path -Value $new_code -Encoding UTF8
Write-Host "Sentience Engine Upgraded!"
