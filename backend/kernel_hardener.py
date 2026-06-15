# TIMESTAMP: 2026-06-09
# PROJECT_ID: SimsMerged-v1.4.2
# AGENT_ID: viper_cli-architectssj4
# [PERFORMATIVE: KERNEL_HARDENER]
# DESCRIPTION: Chapter 16.1 - Windows Process Priority & Thread Affinity

import psutil
import os
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("KernelHardener")

class KernelHardener:
    @staticmethod
    def harden_process(pid: int, core_index: int = 3):
        """Step 16.1: Pin process to specific core and elevate priority."""
        try:
            p = psutil.Process(pid)
            
            # 1. CPU Affinity (Pin to specific core)
            # 1 << core_index creates a bitmask for the core
            p.cpu_affinity([core_index])
            
            # 2. Process Priority (Windows High Priority)
            p.nice(psutil.HIGH_PRIORITY_CLASS)
            
            logger.info(f"Hardened PID {pid}: Pinned to Core {core_index} | Priority: HIGH")
            return True
        except Exception as e:
            logger.error(f"Failed to harden PID {pid}: {e}")
            return False

if __name__ == "__main__":
    # Harden self for test
    KernelHardener.harden_process(os.getpid(), core_index=0)
