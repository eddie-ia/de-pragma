from .database import get_connection

def process_file(file_path):
    import pandas as pd
    df = pd.read_csv(file_path)

    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT count, total_price, min_price, max_price FROM stats WHERE id = 1")
    count, total_price, min_price, max_price = cursor.fetchone()
    count = count or 0
    total_price = total_price or 0.0

    for _, row in df.iterrows():
        price = float(row["price"])
        cursor.execute("INSERT INTO transactions (timestamp, price, user_id) VALUES (?, ?, ?)",
                       (row["timestamp"], price, row["user_id"]))
        count += 1
        total_price += price
        min_price = price if min_price is None else min(min_price, price)
        max_price = price if max_price is None else max(max_price, price)

    cursor.execute("UPDATE stats SET count = ?, total_price = ?, min_price = ?, max_price = ? WHERE id = 1",
                   (count, total_price, min_price, max_price))
    conn.commit()
    conn.close()

def get_stats():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT count, total_price / count AS avg_price, min_price, max_price FROM stats WHERE count > 0")
    result = cursor.fetchone()
    conn.close()
    return result
