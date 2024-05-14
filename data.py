import sqlite3
class Data:
    def __init__(self, file):
        self.db = sqlite3.connect(file)
        self.cursor = self.db.cursor()
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS scoreboard (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT,
                score INTEGER
            )
        """)
        self.db.commit()

    # inserting data into the scoreboard table
    def insert(self, data: tuple):
        query = "INSERT INTO scoreboard (username, score) VALUES (?, ?)"
        self.cursor.execute(query, data)