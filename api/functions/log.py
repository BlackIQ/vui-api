from api.database.sqlite import database


def logger(data):
    cursor, connection = database()

    r = []

    into = ""
    values = ""

    for index, item in enumerate(data):
        if (len(data) == index + 1):
            into += f"{item}"
            values += f"?"
            r.append(data[item])
        else:
            into += f"{item}, "
            values += f"?, "
            r.append(data[item])

    q = f"INSERT INTO LOGS ({into}) VALUES ({values})"

    cursor.execute(q, tuple(r))

    connection.commit()
    connection.close()
