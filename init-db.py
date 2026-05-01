import sqlite3
from werkzeug.security import generate_password_hash

def init_db():
    # Connect to (or create) the database file
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    #create roles tables
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS roles (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            role_name TEXT NOT NULL UNIQUE
        )
    ''')

    # 1. Create Users Table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            role_id INTEGER NOT NULL,
            FOREIGN KEY(role_id) REFERENCES roles(id)
        )
    ''')

    # 2. Create allowed data Table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS allowed_data (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            base_path TEXT NOT NULL,
            allowed_start_date DATE,
            allowed_end_date DATE,
            FOREIGN KEY(user_id) REFERENCES users(id)
        )
    ''')

    # 3. Add Sample Data (Seed Data)
    
    cursor.execute("INSERT OR IGNORE INTO roles (role_name) VALUES ('admin')")
    cursor.execute("INSERT OR IGNORE INTO roles (role_name) VALUES ('user')")
    
    # Let's create an admin and a regular researcher
    users_to_create = [
        ('admin', generate_password_hash('admin123'), 1),
        ('researcher_john', generate_password_hash('hydro2024'), 2)
    ]

    for username, password, role_id in users_to_create:
        try:
            cursor.execute('INSERT INTO users (username, password, role_id) VALUES (?, ?, ?)', (username, password, role_id))
        except sqlite3.IntegrityError:
            print(f"User {username} already exists.")

    # 4. Assign File Paths
    cursor.execute('''
        INSERT INTO allowed_data (user_id, base_path, allowed_start_date, allowed_end_date)
        VALUES (?, ?, ?, ?)
    ''', (2, '/home/data/station_01/', '2024-01-01', '2025-12-31'))
    

    
    conn.commit()
    conn.close()
    print("✅ Database initialized successfully!")

if __name__ == '__main__':
    init_db()