from api.database.sqlite import database
from api.functions.message import send

def notify_admin(message):
    cursor, connection = database()

    cursor.execute(f"SELECT chatid FROM USERS WHERE role = 'god'")
    
    for chatid in cursor.fetchall():
        send(message, chatid[0])

    connection.close()