import sqlite3

class Database:
    def __init__(self):
        self.conn = sqlite3.connect("data/sims_data.db")
        self.cursor = self.conn.cursor()

    def create_tables(self):
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS sims (
                id INTEGER PRIMARY KEY,
                name TEXT NOT NULL,
                age INTEGER NOT NULL
            );
        """)
        self.conn.commit()

    def insert_sim(self, name, age):
        self.cursor.execute("INSERT INTO sims (name, age) VALUES (?, ?);", (name, age))
        self.conn.commit()

    def get_sims(self):
        self.cursor.execute("SELECT * FROM sims;")
        return self.cursor.fetchall()
