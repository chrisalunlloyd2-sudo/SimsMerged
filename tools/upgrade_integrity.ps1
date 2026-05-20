$integrity_path = "C:\Users\viper\Desktop\SimsMerged\backend\core\system_integrity.py"
$new_code = @"
import random

class SystemIntegrity:
    def __init__(self):
        self.purge_count = 0

    def process_stability_net(self, current_stability, attributes=None):
        rag_k = float(attributes.get('rag_k', 10)) if attributes else 10
        mem_limit = float(attributes.get('mem', 24)) if attributes else 24
        
        recovery_rate = 0.005
        purge_threshold = 0.3
        
        recovery_multiplier = rag_k / 10.0
        applied_recovery = recovery_rate * recovery_multiplier
        
        if mem_limit < 16:
            purge_threshold = 0.6
        elif mem_limit > 64:
            purge_threshold = 0.1
            
        should_purge = False
        if current_stability < purge_threshold:
            should_purge = True
            self.purge_count += 1
            
        return {
            'should_purge': should_purge,
            'recovery_increment': float(applied_recovery),
            'purge_threshold': float(purge_threshold),
            'status': 'AGGRESSIVE' if purge_threshold > 0.4 else 'STABLE'
        }
"@
Set-Content -Path $integrity_path -Value $new_code -Encoding UTF8
Write-Host "System Integrity Upgraded!"
