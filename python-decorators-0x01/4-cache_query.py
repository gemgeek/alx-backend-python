#!/usr/bin/python3
import sqlite3
import functools

# cache dictionary to store query results
query_cache = {}

# decorator to handle database connection
def with_db_connection(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        conn = sqlite3.connect("users.db")
        try:
            result = func(conn, *args, **kwargs)
        finally:
            conn.close()
        return result
    return wrapper

# decorator to cache queries
def cache_query(func):
    @functools.wraps(func)
    def wrapper(conn, query, *args, **kwargs):
        if query in query_cache:
            print("Using cached result for query:", query)
            return query_cache[query]
        else:
            print("Executing query and caching result:", query)
            result = func(conn, query, *args, **kwargs)
            query_cache[query] = result
            return result
    return wrapper

@with_db_connection
@cache_query
def fetch_users_with_cache(conn, query):
    cursor = conn.cursor()
    cursor.execute(query)
    return cursor.fetchall()

# First call will cache the result
users = fetch_users_with_cache(query="SELECT * FROM users")
print("First call:", users)

# Second call will use cached result
users_again = fetch_users_with_cache(query="SELECT * FROM users")
print("Second call (cached):", users_again)