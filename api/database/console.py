import sqlite3

# Connect to the SQLite database
conn = sqlite3.connect('vui.db')
cursor = conn.cursor()

# Update the users table
cursor.execute("UPDATE USERS SET access = ?", (True,))

# Commit the changes and close the connection
conn.commit()
conn.close()
