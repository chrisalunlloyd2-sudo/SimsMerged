import os, json, glob

sandbox_dir = "C:/Users/viper/Desktop/SimsMerged/SSD_SANDBOX"
backend_dir = "C:/Users/viper/Desktop/SimsMerged/backend"

todos = set()

# 1. Harvest from JSON files
json_files = glob.glob(sandbox_dir + "/*.json") + glob.glob(backend_dir + "/*.json")
for j_path in json_files:
    try:
        with open(j_path, "r", encoding="utf-8") as f:
            data = json.load(f)
            # Support both direct arrays and object wrappers
            if isinstance(data, dict) and "todos" in data:
                for t in data["todos"]:
                    todos.add(f"[JSON_LIST] {t.strip()}")
            elif isinstance(data, list):
                for item in data:
                    if isinstance(item, dict) and "todo" in item:
                        todos.add(f"[JSON_OBJ] {item['todo'].strip()}")
    except Exception as e:
        pass

# 2. Harvest from Python and JS files
code_files = glob.glob(sandbox_dir + "/**/*.py", recursive=True) + \
             glob.glob(backend_dir + "/**/*.py", recursive=True) + \
             glob.glob(sandbox_dir + "/**/*.js", recursive=True) + \
             glob.glob(backend_dir + "/**/*.js", recursive=True) + \
             glob.glob("C:/Users/viper/Desktop/SimsMerged/frontend/**/*.js", recursive=True)

for fp in code_files:
    try:
        with open(fp, "r", encoding="utf-8") as f:
            for line_no, line in enumerate(f, 1):
                if "TODO:" in line or "TODO " in line:
                    clean_line = line.strip().replace("//", "").replace("#", "").strip()
                    todos.add(f"[CODE] {os.path.basename(fp)} (L{line_no}): {clean_line}")
    except Exception as e:
        pass

# 3. Filter out completed ones
completed_keywords = ["Txt Verifier", "aggregation_utils", "logic_engine_extension", "txt.txt", "VERIFIED"]
filtered_todos = []

for t in todos:
    if not any(c.lower() in t.lower() for c in completed_keywords):
        filtered_todos.append(t)

# 4. Write to FORGOTTEN_TODOS.md
output_path = sandbox_dir + "/FORGOTTEN_TODOS.md"
with open(output_path, "w", encoding="utf-8") as f:
    f.write("# Harvested Forgotten & Broken TODOs\n")
    f.write("[TIMESTAMP: 2026-06-08T03:52:00.000Z]\n\n")
    if not filtered_todos:
        f.write("*No forgotten TODOs found.*")
    else:
        for t in sorted(filtered_todos):
            f.write(f"- {t}\n")

print(f"Harvested {len(filtered_todos)} TODOs. Saved to FORGOTTEN_TODOS.md")
