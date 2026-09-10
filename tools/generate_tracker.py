import os
import re

ROADMAP_PATH = r"C:\Users\viper\Desktop\SimsMerged\docs\MASTER_ROADMAP.md"
OUTPUT_PATH = r"C:\Users\viper\Desktop\SimsMerged\FEATURE_LOGIC_TABLE.md"

def generate_table():
    if not os.path.exists(ROADMAP_PATH):
        print(f"Error: {ROADMAP_PATH} not found.")
        return

    with open(ROADMAP_PATH, "r", encoding="utf-8") as f:
        lines = f.readlines()

    tasks = []
    pattern = re.compile(r"- \[([ xX])\] \*\*(Task|Feature) (\d+):\*\* (.+)")
    for line in lines:
        match = pattern.search(line)
        if match:
            status = "Completed" if match.group(1).lower() == "x" else "Pending"
            task_id = match.group(3)
            desc = match.group(4).strip()
            tasks.append({"id": int(task_id), "desc": desc, "status": status})

    tasks.sort(key=lambda x: x["id"])

    # Define backend mappings based on keywords
    def assign_backend(desc):
        desc_lower = desc.lower()
        if "thread" in desc_lower or "async" in desc_lower or "non-blocking" in desc_lower:
            return "backend/core/system_integrity.py"
        elif "agent" in desc_lower or "neural" in desc_lower or "darwinistic" in desc_lower:
            return "backend/core/agent_lifecycle.py"
        elif "render" in desc_lower or "visual" in desc_lower or "isometric" in desc_lower or "frame" in desc_lower:
            return "frontend/js/engine.js & backend/main.py"
        elif "crypto" in desc_lower or "encrypt" in desc_lower or "purge" in desc_lower:
            return "backend/core/si_inhibitor.py"
        elif "data" in desc_lower or "telemetry" in desc_lower or "packet" in desc_lower:
            return "backend/models/schema.py"
        else:
            return "backend/main.py"

    custom_features = [
        {"phase": "Phase A: High-Fidelity WebUI Polish", "desc": "WebGL 3D Visualizer & Isometric Bridge Sync", "backend": "frontend/js/engine.js, backend/main.py"},
        {"phase": "Phase B: Environment & World Systems", "desc": "Automated Vehicle Traffic & Pathfinding", "backend": "backend/core/agent_lifecycle.py"},
        {"phase": "Phase B: Environment & World Systems", "desc": "Dynamic Weather Simulation Engine", "backend": "backend/core/system_integrity.py"},
        {"phase": "Phase C: Cyber-Economy", "desc": "Advanced AI Trading, Stock Market & Decentralized Storage", "backend": "backend/core/si_inhibitor.py"},
        {"phase": "Phase C: Cyber-Economy", "desc": "Simple Crypto Resource (SimCoin)", "backend": "backend/models/schema.py"},
        {"phase": "Phase D: Urban Venues", "desc": "Hotel Casino Expansion & AI Negotiation protocols", "backend": "backend/core/agent_lifecycle.py"},
        {"phase": "Phase D: Urban Venues", "desc": "Hospital Med-Bay & Agent Recovery Logic", "backend": "backend/core/system_integrity.py"},
        {"phase": "Phase E: Easter Eggs", "desc": "Flappy Bird Arcade Machine Integration", "backend": "frontend/js/bridge.js"}
    ]

    with open(OUTPUT_PATH, "w", encoding="utf-8") as out:
        out.write("# 🧬 SIMSMERGED: MASTER FEATURE LOGIC TABLE & TRACKER\n\n")
        out.write("This table links every procedural feature and newly proposed expansion to its corresponding backend architectural module.\n\n")

        out.write("## 🚀 SENSIBLE NEW ADDITIONS & PHASED ROADMAP\n\n")
        out.write("| Implementation Phase | Feature Description | Backend Target |\n")
        out.write("|----------------------|---------------------|----------------|\n")
        for f in custom_features:
            out.write(f"| {f['phase']} | {f['desc']} | `{f['backend']}` |\n")

        out.write("\n## 🌌 THE 2000+ CORE ROADMAP FEATURES\n\n")
        out.write("*Displaying grouped batches for sanity. All features are tracked linearly.* \n\n")

        out.write("| Task ID | Feature Description | Status | Target Backend Module |\n")
        out.write("|---------|---------------------|--------|-----------------------|\n")

        # Write first 50 and some intervals to avoid making the markdown file literally 2000 lines long,
        # or we can write all of them since it's a file on disk. Let's write all of them, it's just a file.
        for t in tasks:
            mod = assign_backend(t['desc'])
            out.write(f"| {t['id']} | {t['desc']} | {t['status']} | `{mod}` |\n")

    print(f"Successfully generated Logic Table at: {OUTPUT_PATH} with {len(tasks)} core features.")

if __name__ == '__main__':
    generate_table()
