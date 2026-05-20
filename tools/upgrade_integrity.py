import os

integrity_path = r"C:\Users\viper\Desktop\SimsMerged\backend\core\system_integrity.py"

new_code = """
import random

class SystemIntegrity:
    def __init__(self):
        self.purge_count = 0

    def process_stability_net(self, current_stability, attributes=None):
        \"\"\"
        Manages healing and purging logic based on AI research attributes.
        \"\"\"
        # Research Attributes
        rag_k = float(attributes.get('rag_k', 10)) if attributes else 10
        mem_limit = float(attributes.get('mem', 24)) if attributes else 24
        
        recovery_rate = 0.005 # Baseline
        purge_threshold = 0.3 # Baseline
        
        # 1. RAG impact: Better retrieval = faster healing in Sanctuaries
        recovery_multiplier = rag_k / 10.0
        applied_recovery = recovery_rate * recovery_multiplier
        
        # 2. KV Cache impact: Low memory limit makes the system more aggressive at purging
        if mem_limit < 16:
            purge_threshold = 0.6 # Purge much earlier
        elif mem_limit > 64:
            purge_threshold = 0.1 # Very stable, rarely purge
            
        should_purge = False
        if current_stability < purge_threshold:
            should_purge = True
            self.purge_count += 1
            
        return {
            'should_purge': should_purge,
            'recovery_increment': applied_recovery,
            'purge_threshold': purge_threshold,
            'status': 'AGGRESSIVE' if purge_threshold > 0.4 else 'STABLE'
        }
"""

with open(integrity_path, "w", encoding="utf-8") as f:
    f.write(new_code)

print("System Integrity upgraded with research-driven stability logic!")
