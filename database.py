import sqlite3

def get_connection():
    return sqlite3.connect("salvage.db", check_same_thread=False)


def create_tables():
    conn = get_connection()
    cursor = conn.cursor()

    # Vehicles table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS vehicles (
            vehicle_id INTEGER PRIMARY KEY AUTOINCREMENT,
            insurance_company TEXT,
            previous_owner TEXT,
            contact TEXT,
            logbook_number TEXT,
            registration_number TEXT UNIQUE,
            make TEXT,
            model TEXT,
            year INTEGER,
            damage_type TEXT,
            purchase_price REAL,
            status TEXT DEFAULT 'Available'
        )
    """)

    # Buyers table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS buyers (
            buyer_id INTEGER PRIMARY KEY AUTOINCREMENT,
            full_name TEXT,
            phone_number TEXT,
            id_number TEXT
        )
    """)

    # Sales table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS sales (
            sale_id INTEGER PRIMARY KEY AUTOINCREMENT,
            vehicle_id INTEGER,
            buyer_id INTEGER,
            sale_price REAL,
            sale_date TEXT
        )
    """)
    # Users table (for login)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE,
            password TEXT
        )
    """)

    # Default admin
    cursor.execute("SELECT * FROM users WHERE username='admin'")
    if not cursor.fetchone():
        cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)",
                       ("admin", "admin123"))

    conn.commit()
    conn.close()