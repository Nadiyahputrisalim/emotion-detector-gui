import sqlite3

def connect_db(db_name="emotion_database.db"):
    return sqlite3.connect(db_name)

def create_table(conn):
    conn.execute('''
        CREATE TABLE IF NOT EXISTS emotions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT,
            emotion TEXT
        )
    ''')
    conn.commit()

def insert_emotion(conn, timestamp, emotion):
    conn.execute("INSERT INTO emotions (timestamp, emotion) VALUES (?, ?)", (timestamp, emotion))
    conn.commit()
