import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), 'database', 'database.db')

def get_connection():
    return sqlite3.connect(DB_PATH)

def list_tables():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()
    conn.close()
    print("Tables in database:")
    for table in tables:
        print(table[0])

def create_public_messages_table():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS public_messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            senderID INTEGER NOT NULL,
            groupID INTEGER NOT NULL,
            text TEXT NOT NULL,
            date TEXT NOT NULL,
            time TEXT NOT NULL,
            FOREIGN KEY(senderID) REFERENCES users(userID)
        )
    """)
    conn.commit()
    conn.close()

create_public_messages_table()
list_tables()