# [TIMESTAMP: 2026-06-14T15:30:00.000Z] [PROJECT_ID: SimsMerged-v1.4.2] [AGENT_ID: viper_cli-architectssj4]
# ACTION: Headless Agent Tool - AST Analyzer

import ast
import json
import sys

def analyze_ast(filepath):
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()
            
        tree = ast.parse(content)
        
        report = {
            "functions": [],
            "classes": [],
            "missing_docstrings": 0,
            "complex_loops": 0
        }
        
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                report["functions"].append(node.name)
                if not ast.get_docstring(node):
                    report["missing_docstrings"] += 1
            elif isinstance(node, ast.ClassDef):
                report["classes"].append(node.name)
                if not ast.get_docstring(node):
                    report["missing_docstrings"] += 1
            elif isinstance(node, (ast.For, ast.While)):
                for child in ast.walk(node):
                    if child != node and isinstance(child, (ast.For, ast.While)):
                        report["complex_loops"] += 1
                        
        print(json.dumps(report))
        return report
    except Exception as e:
        print(json.dumps({"error": str(e)}))

if __name__ == "__main__":
    if len(sys.argv) > 1:
        analyze_ast(sys.argv[1])
