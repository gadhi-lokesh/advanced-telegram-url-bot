
import sqlite3

DB_NAME = "urls.db"


def get_connection():

    return sqlite3.connect(DB_NAME)


def create_database():

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS urls (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            original_url TEXT NOT NULL,
            short_url TEXT NOT NULL,
            provider TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY,
            username TEXT,
            first_name TEXT
        )
    """)

    conn.commit()
    conn.close()


def save_user(user_id, username, first_name):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO users (user_id, username, first_name)
        VALUES (?, ?, ?)
        ON CONFLICT(user_id) DO UPDATE SET
            username = excluded.username,
            first_name = excluded.first_name
    """, (user_id, username, first_name))

    conn.commit()
    conn.close()


def save_url(user_id, original_url, short_url, provider):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO urls
        (user_id, original_url, short_url, provider)
        VALUES (?, ?, ?, ?)
    """, (user_id, original_url, short_url, provider))

    conn.commit()
    conn.close()


def get_history(user_id):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT original_url, short_url, provider, created_at
        FROM urls
        WHERE user_id = ?
        ORDER BY id DESC
        LIMIT 10
    """, (user_id,))

    records = cursor.fetchall()

    conn.close()

    return records


def get_stats(user_id):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT COUNT(*) FROM urls
        WHERE user_id = ?
    """, (user_id,))

    total = cursor.fetchone()[0]

    conn.close()

    return total
