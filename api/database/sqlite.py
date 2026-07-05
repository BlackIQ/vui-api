import sqlite3

import api.config.config as config

def database():
    connection = sqlite3.connect(config.DB_NAME)
    cursor = connection.cursor()
    return cursor, connection
