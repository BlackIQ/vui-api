import datetime
import sqlite3

# Connect to the SQLite database
conn = sqlite3.connect('vui.db')
cursor = conn.cursor()

timestamp = datetime.datetime.now()

# Update the users table
cursor.execute("UPDATE USERS SET timestamp= ?", (timestamp,))

# Commit the changes and close the connection
conn.commit()
conn.close()
