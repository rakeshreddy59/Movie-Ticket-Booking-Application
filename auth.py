import sqlite3
import hashlib
from database import create_connection

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def verify_password(input_password, stored_password):
    return hash_password(input_password) == stored_password

def signup_user(username, email, password):
    conn = create_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO users (username, email, password) VALUES (?, ?, ?)",
                       (username, email, hash_password(password)))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False
    finally:
        conn.close()

def login_user(email, password):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, password FROM users WHERE email=?", (email,))
    user = cursor.fetchone()
    conn.close()

    if user and verify_password(password, user[1]):
        return user[0]  # return user ID
    return None