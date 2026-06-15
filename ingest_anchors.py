# [TIMESTAMP: 2026-06-12T21:45:00.000Z] [PROJECT_ID: SimsMerged-v1.4.2] [AGENT_ID: viper_cli-architectssj4]
import os
import sys
import ast
import hashlib
import time

# Ensure project root is in sys.path
sys.path.append(os.path.abspath(os.path.dirname(__file__)))

from backend.core.data_syphon_epmo import code_db, Scraper
from backend.core.config import add_log

def ingest_high_value_anchors():
    files_to_scrape = [
        "backend/core/ml_orchestrator.py",
        "backend/core/data_syphon_epmo.py",
        "backend/core/agentic_github_suite.py"
    ]
    
    count = 0
    project_root = "C:\\Users\\viper\\Desktop\\SimsMerged"
    
    for rel_path in files_to_scrape:
        file_path = os.path.join(project_root, rel_path)
        if not os.path.exists(file_path):
            continue
            
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()
            
            tree = ast.parse(content)
            for node in ast.walk(tree):
                if isinstance(node, ast.FunctionDef) and node.body:
                    doc = ast.get_docstring(node)
                    performative = doc if doc else f"High-Value Core: {node.name}"
                    code = ast.get_source_segment(content, node)
                    
                    if code and len(code) > 50:
                        vars = [n.id for n in ast.walk(node) if isinstance(n, ast.Name)]
                        # Block A2 Mandate: Ingest as high-value anchor (Score 10.0)
                        code_db.submit_code(performative, code, list(set(vars)), score=10.0)
                        count += 1
        except Exception as e:
            print(f"Error scraping {rel_path}: {e}")

    print(f"Successfully anchored {count} core methods into Ghost Code DB.")
    add_log(f"[BLOCK_A2] Anchored {count} core methods with priority 10.0.")

if __name__ == "__main__":
    ingest_high_value_anchors()
