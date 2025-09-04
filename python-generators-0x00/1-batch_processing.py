#!/usr/bin/python3
import sqlite3

# Generator to stream users in batches
def stream_users_in_batches(batch_size):
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    cursor.execute("SELECT user_id, name, email, age FROM user_data")

    while True:
        rows = cursor.fetchmany(batch_size)  # fetch 'batch_size' rows
        if not rows:
            break
        batch = []
        for row in rows:
            user = {
                "user_id": row[0],
                "name": row[1],
                "email": row[2],
                "age": row[3],
            }
            batch.append(user)
        yield batch  # yield one batch at a time

    conn.close()


# Function to process batches (filter users over 25)
def batch_processing(batch_size):
    for batch in stream_users_in_batches(batch_size):
        for user in batch:
            if user["age"] > 25:
                print(user)