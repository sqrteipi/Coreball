import sqlite3
import json
def to_dict(t: tuple):
    return {"username": t[0], "score": t[1]}


class Data:
    def __init__(self, file):
        self.db = sqlite3.connect(file)
        self.cursor = self.db.cursor()
        self.data = []
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
        self.db.commit()

    def fetch(self):
        query = "SELECT username, score FROM scoreboard"
        self.cursor.execute(query)
        rows = self.cursor.fetchall()

        # Convert rows to  dictionaries and remove duplicates (if needed)
        data = [to_dict(row) for row in rows]  # List comprehension for concise conversion
        # data = list(set(data))
        print(json.dumps(data))
        # Return JSON-formatted data
        return json.dumps(data)

