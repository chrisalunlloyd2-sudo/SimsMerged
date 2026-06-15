# [TIMESTAMP: 2026-06-14T17:30:00.000Z]
import sys
import os

project_root = r"C:\Users\viper\Desktop\SimsMerged"
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from backend.core.bm25_orchestrator import bm25_scaffold

def populate_ghost_db():
    ghost_python = bm25_scaffold.get_ghost_code("python")
    
    templates = [
        {
            "id": "T1",
            "text": "with open('C:/Users/viper/Desktop/Metropolis_Evolution/heartbeat.txt', 'w') as f: f.write('SOVEREIGN')",
            "lss_weight": 2.0,
            "tags": ["file", "write", "heartbeat"]
        },
        {
            "id": "T2",
            "text": "import subprocess; subprocess.run(['mvn', 'compile'], cwd='C:/Users/viper/Desktop/Metropolis_Evolution/Source/JavaCore', shell=True)",
            "lss_weight": 2.0,
            "tags": ["maven", "compile", "build"]
        },
        {
            "id": "T3",
            "text": "def scaffold_pom(path):\n    pom_content = '<project>...</project>'\n    with open(path, 'w') as f:\n        f.write(pom_content)",
            "lss_weight": 2.0,
            "tags": ["pom", "xml", "scaffold"]
        }
    ]
    
    ghost_python.ingest_corpus(templates)
    print("Ghost Code DB Hydrated with Sovereign Templates.")

if __name__ == "__main__":
    populate_ghost_db()
