#!/usr/bin/python3
"""
seed.py
Sets up the MySQL database ALX_prodev and seeds it with user data from CSV.
"""

import mysql.connector
import csv

# ---------- 1. Connect to MySQL server (no database yet) ----------
def connect_db():
    try:
        connection = mysql.connector.connect(
            host="localhost",      # or your MySQL server host
            user="root",           # change if your MySQL user is different
            password="password"    # put your MySQL root password
        )
        return connection
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return None

# ---------- 2. Create database if not exists ----------
def create_database(connection):
    cursor = connection.cursor()
    cursor.execute("CREATE DATABASE IF NOT EXISTS ALX_prodev;")
    cursor.close()

# ---------- 3. Connect directly to ALX_prodev ----------
def connect_to_prodev():
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="password",
            database="ALX_prodev"
        )
        return connection
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return None

# ---------- 4. Create user_data table ----------
def create_table(connection):
    cursor = connection.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS user_data (
            user_id CHAR(36) PRIMARY KEY,
            name VARCHAR(255) NOT NULL,
            email VARCHAR(255) NOT NULL,
            age DECIMAL NOT NULL,
            INDEX (user_id)
        );
    """)
    connection.commit()
    print("Table user_data created successfully")
    cursor.close()

# ---------- 5. Insert data from CSV ----------
def insert_data(connection, csv_file):
    cursor = connection.cursor()
    with open(csv_file, "r") as file:
        reader = csv.DictReader(file)
        for row in reader:
            cursor.execute("""
                INSERT IGNORE INTO user_data (user_id, name, email, age)
                VALUES (%s, %s, %s, %s);
            """, (row["user_id"], row["name"], row["email"], row["age"]))
    connection.commit()
    cursor.close()