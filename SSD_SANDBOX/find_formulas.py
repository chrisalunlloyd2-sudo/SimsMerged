import sqlite3, os, glob

db_files = glob.glob('C:/Users/viper/Desktop/SimsMerged/SSD_SANDBOX/*.db') + glob.glob('C:/Users/viper/Desktop/SimsMerged/SSD_SANDBOX/agent_memories/*.db')
found = False
for db in db_files:
    try:
        conn = sqlite3.connect(db)
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = cursor.fetchall()
        for table in tables:
            table_name = table[0]
            cursor.execute(f"PRAGMA table_info({table_name})")
            columns = [info[1] for info in cursor.fetchall()]
            for col in columns:
                try:
                    cursor.execute(f"SELECT * FROM {table_name} WHERE {col} LIKE '%formula%' OR {col} LIKE '%tok%tree%'")
                    rows = cursor.fetchall()
                    for row in rows:
                        print(f"FOUND IN {db} -> Table {table_name}: {row}")
                        found = True
                except Exception:
                    pass
    except Exception:
        pass

if not found:
    print('NO_FORMULAS_IN_SQLITE')
