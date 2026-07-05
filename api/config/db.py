from api.database.sqlite import database

def load_configs():
    cursor, conn = database()
    cursor.execute("SELECT key, value FROM CONFIGS")
    rows = cursor.fetchall()
    conn.close()
    return {key: value for key, value in rows}


CONFIGS = load_configs()

PORT = int(CONFIGS.get("port", 5000))
KEY = CONFIGS.get("key", "")
SECRET = CONFIGS.get("secret", "")
