import sqlite3
from pathlib import Path

# Define database location
DB_PATH = Path(__file__).resolve().parent.parent / "outputs" / "prueba_datos.db"

def get_connection():
    '''Returns a new connection to the SQLite database'''
    return sqlite3.connect(DB_PATH)

def setup_database():
    """
    Creates the required tables 
    and initializes the stats row if needed
    """
    with get_connection() as conn:
        cursor = conn.cursor()

        # Create transactions table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS transactions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT,
                price REAL,
                user_id TEXT
            )
        """)

        # Create stats table (update or create, only one row)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS stats (
                id INTEGER PRIMARY KEY CHECK (id = 1),
                count INTEGER,
                total_price REAL,
                min_price REAL,
                max_price REAL
            )
        """)

        # Initialize stats row if it's empty
        cursor.execute("SELECT COUNT(*) FROM stats")
        row_exists = cursor.fetchone()[0]
        if row_exists == 0:
            cursor.execute("""
                INSERT INTO stats (id, count, total_price, min_price, max_price)
                VALUES (1, 0, 0, NULL, NULL)
            """)

        conn.commit()
