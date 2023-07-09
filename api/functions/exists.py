from api.database.sqlite import database

def exists(username):
    cursor, connection = database()

    cursor.execute(f"SELECT COUNT(*) AS c FROM USERS WHERE username = ?", (username,))

    count = cursor.fetchone()[0]

    connection.close()

    return count