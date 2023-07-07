import sqlite3

# Connect to the SQLite database
conn = sqlite3.connect('vui.db')
cursor = conn.cursor()

# Create the users table
cursor.execute('''
    CREATE TABLE IF NOT EXISTS USERS (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username VARCHAR(50),
        password VARCHAR(50),
        role VARCHAR(50),
        owner VARCHAR(50)
    )
''')

# Commit the changes and close the connection
conn.commit()
conn.close()
