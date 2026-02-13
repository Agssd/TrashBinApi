import sqlite3

DB_PATH = "app/database.db"

def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            login TEXT NOT NULL UNIQUE,
            password TEXT NOT NULL,
            points INTEGER DEFAULT 0
        )
    ''')
    
    c.execute('''
        CREATE TABLE IF NOT EXISTS trash_bins (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            platform_number TEXT,
            schedule TEXT,
            longitude REAL NOT NULL,
            latitude REAL NOT NULL,
            district TEXT,
            fill_level INTEGER DEFAULT 0
        )
    ''')
    
    c.execute('''
        CREATE TABLE IF NOT EXISTS scanned_bins (
            bin_id INTEGER,
            user_id INTEGER, 
            scanned_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            PRIMARY KEY (bin_id, user_id)
        )
    ''')
    conn.commit()
    conn.close()

def get_db():
    return sqlite3.connect(DB_PATH)