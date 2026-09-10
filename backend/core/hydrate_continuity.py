# [TIMESTAMP: 2026-06-14T16:00:00.000Z]
import sys
import os

project_root = r"C:\Users\viper\Desktop\SimsMerged"
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from backend.core.bm25_orchestrator import bm25_scaffold

def hydrate():
    mandate_path = os.path.join(project_root, "SSD_SANDBOX", "ASCENSION_MANDATE.md")
    with open(mandate_path, "r", encoding="utf-8") as f:
        mand = f.read()

    bm25_scaffold.continuity.update_learning(mand, metadata={"type": "mandate", "lss_weight": 2.0})

    # Also add workspace info
    workspace_info = "Metropolis_Evolution is the agents primary workspace for rebuilding the game. It is located at C:/Users/viper/Desktop/Metropolis_Evolution. Source/JavaCore contains the JavaFX Neo engine."
    bm25_scaffold.continuity.update_learning(workspace_info, metadata={"type": "workspace", "lss_weight": 2.0})

    print("Continuity Hydrated Successfully.")

if __name__ == "__main__":
    hydrate()
