import sqlite3

# Connect to the SQLite database
conn = sqlite3.connect('vui.db')
cursor = conn.cursor()

# Create the users table
cursor.execute('''
    ALTER TABLE USERS ADD COLUMN name VARCHAR(50)
''')

# Commit the changes and close the connection
conn.commit()
conn.close()
