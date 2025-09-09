#!/usr/bin/python3
import sqlite3
import functools

# decorator to handle database connections
def with_db_connection(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        conn = sqlite3.connect("users.db")  # open connection
        try:
            result = func(conn, *args, **kwargs)
        finally:
            conn.close()  # close connection safely
        return result
    return wrapper

# decorator to handle transactions (commit/rollback)
def transactional(func):
    @functools.wraps(func)
    def wrapper(conn, *args, **kwargs):
        try:
            result = func(conn, *args, **kwargs)  # run the SQL
            conn.commit()  # commit if no error
            return result
        except Exception as e:
            conn.rollback()  # rollback if error happens
            print("Transaction failed, rolled back:", e)
            raise
    return wrapper

@with_db_connection
@transactional
def update_user_email(conn, user_id, new_email):
    cursor = conn.cursor()
    cursor.execute("UPDATE users SET email = ? WHERE id = ?", (new_email, user_id))

# Test: update email of user with id=1
update_user_email(user_id=1, new_email="Crawford_Cartwright@hotmail.com")
print("Email updated successfully")