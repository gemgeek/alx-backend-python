#!/usr/bin/python3
import sqlite3

# Generator that yields users over 25 one by one
def batch_processing(batch_size):
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    cursor.execute("SELECT user_id, name, email, age FROM user_data")

    while True:
        rows = cursor.fetchmany(batch_size)
        if not rows:
            break
        for row in rows:
            user = {
                "user_id": row[0],
                "name": row[1],
                "email": row[2],
                "age": row[3]
            }
            if user["age"] > 25:
                yield user  # yield each user individually

    cursor.close()
    conn.close()

