#!/usr/bin/env python3
"""
Logging Database Queries
"""

import sqlite3
import functools


# 🔹 decorator to log SQL queries
def log_queries(func):
    @functools.wraps(func)  # keeps original function name & docstring
    def wrapper(query, *args, **kwargs):
        print(f"Executing SQL Query: {query}")  # log the query
        return func(query, *args, **kwargs)     # call the original function
    return wrapper


@log_queries
def fetch_all_users(query):
    """Fetch all users from the database using the provided query."""
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute(query)
    results = cursor.fetchall()
    conn.close()
    return results


# 🔹 Test run
if __name__ == "__main__":
    users = fetch_all_users("SELECT * FROM users")
    print(users)