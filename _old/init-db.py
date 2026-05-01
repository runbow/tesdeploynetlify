import sqlite3
from werkzeug.security import generate_password_hash

def init_db():
    # Connect to (or create) the database file
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    # 1. Create Users Table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
    ''')

    # 2. Create Permissions Table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS user_permissions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            file_path TEXT NOT NULL,
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
    ''')

    # 3. Add Sample Data (Seed Data)
    # Let's create an admin and a regular researcher
    users_to_create = [
        ('admin', generate_password_hash('admin123')),
        ('researcher_john', generate_password_hash('hydro2024'))
    ]

    for username, password in users_to_create:
        try:
            cursor.execute('INSERT INTO users (username, password) VALUES (?, ?)', (username, password))
        except sqlite3.IntegrityError:
            print(f"User {username} already exists.")

    # 4. Assign File Paths
    # We'll give 'admin' (ID 1) access to all files, and 'john' (ID 2) only to one.
    permissions = [
        (1, 'data/station_A_2023.csv'),
        (1, 'data/station_B_2023.csv'),
        (2, 'data/station_A_2023.csv') # John can only see Station A
    ]

    cursor.executemany('INSERT INTO user_permissions (user_id, file_path) VALUES (?, ?)', permissions)

    conn.commit()
    conn.close()
    print("✅ Database initialized successfully!")

if __name__ == '__main__':
    init_db()