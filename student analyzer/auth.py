from database import connect_db

def register_user(username, password):
    conn = connect_db()
    cur = conn.cursor()
    cur.execute("INSERT INTO users VALUES (?, ?)", (username, password))
    conn.commit()
    conn.close()

def login_user(username, password):
    conn = connect_db()
    cur = conn.cursor()
    cur.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password))
    result = cur.fetchone()
    conn.close()
    return result