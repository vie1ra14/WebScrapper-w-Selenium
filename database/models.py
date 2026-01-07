import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).parent / "database.db"

def get_connection():
    return sqlite3.connect(DB_PATH)

def create_table():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS jobs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT,
            company TEXT,
            location TEXT,
            collected_at TEXT,
            UNIQUE(title, company, location)
        )
    """)
    conn.commit()
    conn.close()

def insert_job(title, company, location, collected_at):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT OR IGNORE INTO jobs (title, company, location, collected_at)
        VALUES (?, ?, ?, ?)
    """, (title, company, location, collected_at))

    conn.commit()
    conn.close()

def fetch_jobs():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT title, company, location, collected_at FROM jobs")
    rows = cursor.fetchall()
    conn.close()
    return rows

