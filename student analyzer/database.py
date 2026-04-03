import sqlite3

def connect_db():
    return sqlite3.connect("students.db", check_same_thread=False)

def create_tables():
    conn = connect_db()
    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS users(
        username TEXT,
        password TEXT
    )
    """)

    conn.commit()
    conn.close()