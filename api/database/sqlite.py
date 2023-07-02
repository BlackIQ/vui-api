import sqlite3


def database():
    connection = sqlite3.connect('vui.db')
    cursor = connection.cursor()
    return cursor, connection
