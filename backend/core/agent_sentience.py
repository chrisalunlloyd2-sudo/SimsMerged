# TIMESTAMP: 2026-05-25T01:43:00.000Z
# PROJECT_ID: SimsMerged-v1.3
# AGENT_ID: Antigravity-Agent

import random
from enum import Enum
from backend.core import llm_client

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
        Decides the next action for an agent using projected neural inference layers.
        """
        agent_id = agent_data.get('id', 'default')
        energy = agent_data.get('energy', 100)
        stability = agent_data.get('stability', 1.0)
        role = agent_data.get('role', 'PROCESS_KERNEL')
        
        # 1. Dual-Watchdog Safety Check
        if not (self.watchdog_a_active and self.watchdog_b_active):
            return {
                'action': 'HALT',
                'emotional_state': 'UNSAFE',
                'confidence': 0,
                'model_info': self.model_name,
                'watchdog_status': "TRIPPED"
            }

        # 2. Check for Playback Mode
        if agent_data.get('script_id'):
            return {
                'action': 'PLAYBACK',
                'script_id': agent_data['script_id'],
                'emotional_state': 'STABLE',
                'confidence': 1.0,
                'model_info': self.model_name,
                'watchdog_status': "DUAL_LOCKED"
            }

        # 3. Read active AI research attributes
        temp = float(attributes.get('temp', 0.7)) if attributes else 0.7
        top_p = float(attributes.get('top_p', 0.9)) if attributes else 0.9
        
        # 4. Construct Feature State Vector
        # Maps stability, energy percent, role bias and fatigue into a vector
        role_bias = 0.8 if role in ['DOCTOR', 'TEACHER'] else 0.2
        state_vector = [
            float(stability),
            float(energy / 100.0),
            float(role_bias),
            float((100.0 - energy) / 100.0)
        ]
        
        # 5. Run Danube Neural Inference Projection
        action, prob = llm_client.project_danube_inference(state_vector, temp=temp, top_p=top_p)
        
        # 6. Apply vocational constraints for critical tasks
        if role == 'DOCTOR' and stability < 0.6:
            action = 'heal'
        elif role == 'TEACHER' and random.random() < 0.5:
            action = 'teach'
            
        # 7. Determine Emotional State
        state = EmotionalState.STABLE
        if stability < 0.2:
            state = EmotionalState.DEPRESSED
        elif stability < 0.5:
            state = EmotionalState.STRESSED
        if temp > 1.2:
            state = EmotionalState.ERRATIC

        # 8. Script Recording Logic
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
            'confidence': float(prob),
            'model_info': self.model_name,
            'recording': True,
            'watchdog_status': "DUAL_LOCKED"
        }
