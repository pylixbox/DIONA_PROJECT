import sqlite3
import bcrypt

DB_NAME = "diona_system.db"

def init_db():
    conn = sqlite3.connect(DB_NAME)
    # 1. Admin Users Table (ILO 3: Security)
    conn.execute('''CREATE TABLE IF NOT EXISTS users 
                 (id INTEGER PRIMARY KEY AUTOINCREMENT, 
                  username TEXT UNIQUE, password_hash TEXT, role TEXT)''')
    
    # 2. Alerts Table (Tier 3 Persistence)
    conn.execute('''CREATE TABLE IF NOT EXISTS alerts 
                 (id INTEGER PRIMARY KEY AUTOINCREMENT, 
                  attack_type TEXT, attacker_ip TEXT, severity TEXT, 
                  timestamp DATETIME DEFAULT CURRENT_TIMESTAMP)''')
    
    # 3. Seed Mock Admins (Evidence for Material 3)
    try:
        admins = [('felix', 'f123'), ('gezelle', 'g123'), ('james', 'j123')]
        for user, pwd in admins:
            # Encrypt password before storing in database
            hashed = bcrypt.hashpw(pwd.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
            conn.execute("INSERT INTO users (username, password_hash, role) VALUES (?, ?, ?)", 
                         (user, hashed, 'SuperAdmin'))
        conn.commit()
    except: pass # Prevents crash if users already exist
    conn.close()

# Runs only when file is executed directly
if __name__ == "__main__":
    init_db()
    print("Tier 3 Initialized: SQLite Database Created.")