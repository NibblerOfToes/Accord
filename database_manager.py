import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), 'database', 'database.db')

def get_connection():
    return sqlite3.connect(DB_PATH)

def validate_user(email, password):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE email = ? AND password = ?", (email, password))
    user = cursor.fetchone()
    conn.close()
    return user  # returns None if not found

def listExtension():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT name, email FROM users")
    results = cursor.fetchall()
    conn.close()
    return results