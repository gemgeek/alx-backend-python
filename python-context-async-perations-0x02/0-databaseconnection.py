import sqlite3

# Step 1: Define the context manager class
class DatabaseConnection:
    def __init__(self, db_name):
        self.db_name = db_name
        self.conn = None

    def __enter__(self):
        # This runs when we enter the 'with' block
        self.conn = sqlite3.connect(self.db_name)
        return self.conn  # return the connection so we can use it

    def __exit__(self, exc_type, exc_value, traceback):
        # This always runs when leaving the 'with' block
        if self.conn:
            self.conn.close()
        # Returning False means errors will not be suppressed
        return False


# Step 2: Use the context manager
with DatabaseConnection("users.db") as conn:
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users")
    results = cursor.fetchall()
    print(results)