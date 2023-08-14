import datetime
import sqlite3

# Connect to the SQLite database
conn = sqlite3.connect('vui.db')
cursor = conn.cursor()

timestamp = datetime.datetime.now()
expire = timestamp + datetime.timedelta(days=30)

# Update the users table
cursor.execute("UPDATE USERS SET expire= ?", (expire,))

# Commit the changes and close the connection
conn.commit()
conn.close()
