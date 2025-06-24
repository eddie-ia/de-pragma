import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).resolve().parent.parent / "outputs" / "prueba_datos.db"

def get_connection():
    return sqlite3.connect(DB_PATH)

def setup_database():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS transactions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT,
            price REAL,
            user_id TEXT
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS stats (
            id INTEGER PRIMARY KEY CHECK (id = 1),
            count INTEGER,
            total_price REAL,
            min_price REAL,
            max_price REAL
        )
    """)
    cursor.execute("SELECT COUNT(*) FROM stats")
    if cursor.fetchone()[0] == 0:
        cursor.execute("INSERT INTO stats (id, count, total_price, min_price, max_price) VALUES (1, 0, 0, NULL, NULL)")
    conn.commit()
    conn.close()
