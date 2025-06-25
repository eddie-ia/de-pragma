from .database import get_connection
import pandas as pd

def process_file(file_path):
    """
    Processes a CSV file: inserts transactions into the database
    and updates the global statistics incrementally.
    """
    df = pd.read_csv(file_path)

    with get_connection() as conn:
        cursor = conn.cursor()

        # Fetch current stats
        cursor.execute("""
            SELECT count, total_price, min_price, max_price 
            FROM stats 
            WHERE id = 1
        """)
        count, total_price, min_price, max_price = cursor.fetchone()

        # Fallback in case of NULLs (initial state)
        count = count or 0
        total_price = total_price or 0.0

        # Process each row
        for row in df.itertuples(index=False):
            price = float(row.price)
            cursor.execute("""
                INSERT INTO transactions (timestamp, price, user_id)
                VALUES (?, ?, ?)
            """, (row.timestamp, price, row.user_id))

            # Update stats
            count += 1
            total_price += price
            min_price = price if min_price is None else min(min_price, price)
            max_price = price if max_price is None else max(max_price, price)

        # Update the single stats row
        cursor.execute("""
            UPDATE stats
            SET count = ?, total_price = ?, min_price = ?, max_price = ?
            WHERE id = 1
        """, (count, total_price, min_price, max_price))

        conn.commit()


def get_stats():
    """
    Retrieves current aggregated statistics from the database.
    Returns (count, average, min, max) or (None, None, None, None) if empty.
    """
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT count, total_price * 1.0 / count AS avg_price, min_price, max_price
            FROM stats
            WHERE count > 0
        """)
        return cursor.fetchone()
