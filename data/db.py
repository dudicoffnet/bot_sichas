import sqlite3
import os

DB_PATH = os.path.join("data", "users.db")

def init_db():
    os.makedirs("data", exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("""CREATE TABLE IF NOT EXISTS users (
        user_id INTEGER PRIMARY KEY,
        name TEXT,
        age INTEGER,
        gender TEXT,
        location TEXT,
        activities TEXT,
        is_free INTEGER DEFAULT 0
    )""")
    conn.commit()
    conn.close()

def save_user(user_id, name=None, age=None, gender=None, location=None, activities=None):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("INSERT OR IGNORE INTO users (user_id) VALUES (?)", (user_id,))
    if name is not None:
        c.execute("UPDATE users SET name=? WHERE user_id=?", (name, user_id))
    if age is not None:
        c.execute("UPDATE users SET age=? WHERE user_id=?", (age, user_id))
    if gender is not None:
        c.execute("UPDATE users SET gender=? WHERE user_id=?", (gender, user_id))
    if location is not None:
        c.execute("UPDATE users SET location=? WHERE user_id=?", (location, user_id))
    if activities is not None:
        c.execute("UPDATE users SET activities=? WHERE user_id=?", (activities, user_id))
    conn.commit()
    conn.close()

def set_free(user_id, is_free: bool):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("UPDATE users SET is_free=? WHERE user_id=?", (1 if is_free else 0, user_id))
    conn.commit()
    conn.close()

def get_matches(activity_like: str):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT user_id, name, age, gender, location, activities FROM users WHERE activities LIKE ? AND is_free=1", (f'%{activity_like}%',))
    rows = c.fetchall()
    conn.close()
    return rows
