import sqlite3

def connect_db(db_name):
    # Koneksi ke database SQLite
    conn = sqlite3.connect(db_name)
    return conn

def fetch_emotions(conn):
    # Mengambil data emosi dari database
    query = "SELECT * FROM emotions"
    cursor = conn.cursor()
    cursor.execute(query)
    rows = cursor.fetchall()
    return rows
