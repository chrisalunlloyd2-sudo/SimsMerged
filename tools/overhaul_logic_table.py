import os
import re

ROADMAP_PATH = r"C:\Users\viper\Desktop\SimsMerged\docs\MASTER_ROADMAP.md"
OUTPUT_PATH = r"C:\Users\viper\Desktop\SimsMerged\FEATURE_LOGIC_TABLE.md"

def overhaul_logic():
    if not os.path.exists(ROADMAP_PATH):
        return

    with open(ROADMAP_PATH, "r", encoding="utf-8") as f:
        content = f.read()

    # Extract all tasks
    pattern = re.compile(r"- \[([ xX])\] \*\*(Task|Feature) (\d+):\*\* (.+)")
    matches = pattern.findall(content)

    groups = {
        "CORE_KERNEL": {
            "keywords": ["thread", "async", "non-blocking", "frame", "bridge", "bus", "sync", "quantum", "core", "kernel", "logic", "protocol"],
            "desc": "The foundational low-level engine managing instruction pipelines and system integrity.",
            "subgroups": {}
        },
        "AGENT_SENTIENCE": {
            "keywords": ["agent", "neural", "darwinistic", "sentience", "emotional", "title", "role", "social", "negotiate"],
            "desc": "AI citizens and their evolving cognitive, social, and vocational models.",
            "subgroups": {}
        },
        "CYBER_ECONOMY": {
            "keywords": ["crypto", "mint", "bank", "stock", "trade", "ledger", "depin", "transaction", "wealth", "balance"],
            "desc": "The decentralized financial infrastructure and simulation of agent-driven markets.",
            "subgroups": {}
        },
        "ENVIRONMENT_HARDWARE": {
            "keywords": ["render", "visual", "isometric", "thermal", "heat", "cool", "water", "tree", "grid", "packet", "telemetry"],
            "desc": "Physical grid properties, hardware simulation, and real-time visualization systems.",
            "subgroups": {}
        },
        "SECURITY_DEFENSE": {
            "keywords": ["cryptographic", "encrypt", "purge", "audit", "hammer", "leakage", "threat", "mitigate", "protection"],
            "desc": "Metropolis protection protocols, hashed memory integrity, and threat neutralization.",
            "subgroups": {}
        }
    }

    definitions = {
        "Non-blocking": "Execution that doesn't halt the system while waiting for I/O.",
        "Asynchronous": "Operations running independently of the main program flow.",
        "Hyper-spectral": "Multi-layered data analysis across the entire frequency spectrum.",
        "Neural": "Mimicking biological brain structures for decision weight alignment.",
        "Sub-atomic": "Logic operating at the smallest unit of instruction granularity.",
        "Cryptographic": "Secured via high-fidelity mathematical hashing (SHA-256).",
        "Recursive": "A process that references itself for continuous self-optimization.",
        "Temporal": "Time-sensitive logic mapping that accounts for system drift.",
        "Darwinistic": "Evolutionary algorithms where the most efficient code survives.",
        "Isometric": "A 2D rendering style that simulates 3D depth and perspective.",
        "Heuristic": "Practical problem-solving logic that doesn't guarantee perfection but is efficient.",
        "Elastic": "Dynamic scaling that expands/contracts based on active system load.",
        "Quantum": "Probabilistic logic states allowing for super-positioned execution.",
        "Zero-latency": "Instruction processing with negligible delay via hardware hooks.",
        "DePIN": "Decentralized Physical Infrastructure Networks linked to the real host.",
        "Purge": "The systematic removal of corrupted or redundant data chunks."
    }

    final_table = []
    
    for m in matches:
        status = "VERIFIED" if m[0].lower() == "x" else "ENACTING"
        task_id = int(m[2])
        raw_desc = m[3].strip()
        
        # Determine Group
        assigned_group = "CORE_KERNEL"
        for g_name, g_data in groups.items():
            if any(k in raw_desc.lower() for k in g_data["keywords"]):
                assigned_group = g_name
                break
        
        # Build Articulate Definition
        def_parts = []
        for word, d in definitions.items():
            if word.lower() in raw_desc.lower():
                def_parts.append(d)
        
        if not def_parts:
            def_parts = ["Procedural logic step for city evolution."]
            
        long_desc = f"{raw_desc} - This protocol ensures system-wide stability by leveraging { ' and '.join(def_parts).lower() }"
        
        final_table.append({
            "id": task_id,
            "group": assigned_group,
            "desc": raw_desc,
            "status": status,
            "definition": long_desc
        })

    # Write Updated TABLE
    with open(OUTPUT_PATH, "w", encoding="utf-8") as out:
        out.write("# ðŸ§¬ SIMSMERGED: HIERARCHICAL FEATURE LOGIC TABLE\n\n")
        out.write("This table categorizes all 2,200+ features into logical hierarchies and defines their system role.\n\n")
        
        for g_name, g_data in groups.items():
            out.write(f"## {g_name.replace('_', ' ')}\n")
            out.write(f"*{g_data['desc']}*\n\n")
            out.write("| ID | Feature | Status | Logical Definition |\n")
            out.write("|----|---------|--------|--------------------|\n")
            
            group_tasks = [t for t in final_table if t["group"] == g_name]
            # To avoid making a 10MB markdown, we show first 20 and summarize
            for t in group_tasks[:20]:
                out.write(f"| {t['id']} | {t['desc']} | {t['status']} | {t['definition']} |\n")
            
            if len(group_tasks) > 20:
                out.write(f"| ... | ... | ... | *{len(group_tasks) - 20} more tasks logically mapped...* |\n")
            out.write("\n")

    print(f"Logic Table Overhauled: {len(final_table)} features grouped and defined.")

if __name__ == "__main__":
    overhaul_logic()
