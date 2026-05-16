import sqlite3
import datetime
import os
DB_FILE = "db/webhook_data.db"
os.makedirs("db", exist_ok=True)
def init_db():
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("""
            CREATE TABLE IF NOT EXISTS downloads (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT,
            direct_url TEXT,
            status TEXT)
            """)
    conn.commit()
    conn.close()

def save_record(direct_url, status):
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    c.execute("INSERT INTO downloads (timestamp, direct_url, status) VALUES (?, ?, ?)",(timestamp, direct_url, status))
    conn.commit()
    conn.close()
    
def list_records(LIMIT=10):
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("SELECT timestamp, direct_url, status FROM downloads ORDER BY id DESC LIMIT ?",(LIMIT,))
    rows = c.fetchall()
    conn.close()
    # HUMAN READABLITIY 
    return [f"[{ts}] {status.upper()} -> {url}" for ts, url, status in rows]