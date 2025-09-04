#!/usr/bin/python3
import mysql.connector

def stream_users():
    """
    Generator function that streams rows from the user_data table one by one.
    Each row is returned as a dictionary.
    """
    # Connect to the database
    connection = mysql.connector.connect(
        host="localhost",
        user="root",       
        password="",       
        database="ALX_prodev"
    )
    cursor = connection.cursor(dictionary=True)  # dictionary=True gives rows as dicts

    # Execute query
    cursor.execute("SELECT * FROM user_data;")

    # Yield one row at a time
    for row in cursor:
        yield row

    # Close cursor and connection
    cursor.close()
    connection.close()