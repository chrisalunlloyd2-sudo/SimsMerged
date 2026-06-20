# TIMESTAMP: 2026-06-09
# PROJECT_ID: SimsMerged-v1.4.2
# AGENT_ID: viper_cli-architectssj4
# [PERFORMATIVE: THERMODYNAMIC_DIFFUSION]
# DESCRIPTION: Chapter 13.3 - Thermodynamic Heat Diffusion Engine

import numpy as np
import json
import os
import logging
import time

logger = logging.getLogger("PhysicsEngine")
logger.setLevel(logging.INFO)

class ThermalGrid:
    def __init__(self, size=100, alpha=0.1):
        """
        size: Grid dimensions (100x100)
        alpha: Diffusion constant (thermal conductivity)
        """
        self.size = size
        self.alpha = alpha
        # Initialize with ambient temperature (20C)
        self.temperature_matrix = np.full((size, size), 20.0, dtype=np.float32)

        # Add some initial heat sources for testing
        self.temperature_matrix[10, 10] = 500.0 # A "Fire" entity
        self.temperature_matrix[50, 50] = -50.0 # A "Frost" entity

    def step(self):
        """Step 13.3: Heat Diffusion Formula f(T) = alpha * grad^2 T"""
        # Vectorized Laplacian using np.roll (Zero-padding/Periodic boundaries simplified)
        T = self.temperature_matrix
        laplacian = (
            np.roll(T, 1, axis=0) + np.roll(T, -1, axis=0) +
            np.roll(T, 1, axis=1) + np.roll(T, -1, axis=1) -
            4 * T
        )
        self.temperature_matrix += self.alpha * laplacian

        # Maintain constant heat sources (Step 8: Thermal Convection Entities)
        self.temperature_matrix[10, 10] = 500.0
        self.temperature_matrix[50, 50] = -50.0

    def save_state(self, filepath=r"C:\Users\viper\Desktop\SimsMerged\backend\thermal_map.json"):
        """Serialize current heat map for JavaFX visualization."""
        # Quantize to int for smaller JSON payload
        data = {
            "matrix": self.temperature_matrix.astype(int).tolist()
        }
        with open(filepath, "w") as f:
            json.dump(data, f)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    engine = ThermalGrid(100)

    logger.info("Simulating 50 steps of heat diffusion...")
    for _ in range(50):
        engine.step()

    engine.save_state()
    logger.info("Thermal state saved for GUI verification.")
