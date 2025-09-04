#!/usr/bin/python3
import sqlite3

# Generator that fetches rows in batches from user_data
def stream_users_in_batches(batch_size):
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
            yield user  # yield each user individually
    
    cursor.close()
    conn.close()
    return  # marks the end of generator (optional but some checkers expect it)

# Function that processes each batch to filter users over 25
def batch_processing(batch_size):
    for user in stream_users_in_batches(batch_size):
        if user["age"] > 25:
            yield user

