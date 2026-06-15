# [TIMESTAMP: 2026-06-14T15:35:00.000Z] [PROJECT_ID: SimsMerged-v1.4.2] [AGENT_ID: viper_cli-architectssj4]
# ACTION: Headless Agent Tool - Security/PII Scanner

import re
import json
import sys

def scan_security(filepath):
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()
            
        report = {
            "pii_flags": [],
            "entropy_warnings": []
        }
        
        # Check for paths
        if re.search(r'[A-Z]:\\[\w\\]+', content) or re.search(r'/home/\w+/', content):
            report["pii_flags"].append("Local absolute path detected.")
            
        # Check for obvious keys
        if re.search(r'(?i)(api_key|secret|password|token)[\s=:]+[\'"]?[\w\-]{8,}[\'"]?', content):
            report["entropy_warnings"].append("Potential high-entropy secret detected.")
            
        print(json.dumps(report))
        return report
    except Exception as e:
        print(json.dumps({"error": str(e)}))

if __name__ == "__main__":
    if len(sys.argv) > 1:
        scan_security(sys.argv[1])
