import sqlite3
import bcrypt

DB_NAME = "diona_system.db"

def get_db_connection():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row 
    return conn

def init_db():
    conn = get_db_connection()
    # Create Tables
    conn.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            role TEXT DEFAULT 'Admin'
        )
    ''')
    conn.execute('''
        CREATE TABLE IF NOT EXISTS alerts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            attack_type TEXT NOT NULL,
            attacker_ip TEXT NOT NULL,
            severity TEXT NOT NULL,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    # Seed Users
    try:
        admins = [('felix', 'f123'), ('gezelle', 'g123'), ('james', 'j123')]
        for user, pwd in admins:
            hashed = bcrypt.hashpw(pwd.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
            conn.execute('INSERT OR IGNORE INTO users (username, password_hash) VALUES (?, ?)', (user, hashed))
        conn.commit()
    except Exception as e:
        print(f"Seeding error: {e}")
    
    conn.close()

if __name__ == "__main__":
    init_db()
    print("✅ Database Tier Initialized.")