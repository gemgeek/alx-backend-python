#!/usr/bin/env python3
import sqlite3

class ExecuteQuery:
    def __init__(self, query, params=None, db_name="example.db"):
        """Initialize with query, parameters, and database name"""
        self.query = query
        self.params = params if params else ()
        self.db_name = db_name
        self.conn = None
        self.cursor = None
        self.results = None

    def __enter__(self):
        """Open connection, execute query, and return results"""
        self.conn = sqlite3.connect(self.db_name)
        self.cursor = self.conn.cursor()
        self.cursor.execute(self.query, self.params)
        self.results = self.cursor.fetchall()
        return self.results  # The results will be available in 'with' block

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Close cursor and connection safely"""
        if self.cursor:
            self.cursor.close()
        if self.conn:
            self.conn.close()
        # Returning False will propagate exceptions if they occur
        return False


# 🔹 Example Usage
if __name__ == "__main__":
    query = "SELECT * FROM users WHERE age > ?"
    params = (25,)
    
    with ExecuteQuery(query, params) as results:
        print("Users older than 25:")
        for row in results:
            print(row)