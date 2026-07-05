import sqlite3

from api.config.config import DB_NAME

# Connect to the SQLite database
conn = sqlite3.connect(DB_NAME)
cursor = conn.cursor()

# Create the users table
cursor.execute('''
    CREATE TABLE IF NOT EXISTS USERS (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username VARCHAR(50),
        password VARCHAR(50)
    )
''')

# Create the clients table
cursor.execute('''
    CREATE TABLE IF NOT EXISTS CLIENTS (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name VARCHAR(50),
        username VARCHAR(50),
        password VARCHAR(50),
        access BOOLEAN
    )
''')

# Create the config table
cursor.execute('''
    CREATE TABLE IF NOT EXISTS CONFIGS (
        key VARCHAR(50),
        value VARCHAR(50)
    )
''')

# Commit the changes and close the connection
conn.commit()
conn.close()
