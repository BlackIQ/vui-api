# Flask
from flask import Flask, request, jsonify
from flask_cors import CORS

# Python libs
import datetime
import os

# Database
from api.database.sqlite import database

# Middlewares
from api.middlewares.apikey import apiKey

# Config
from api.config.config import path

# Functions
from api.functions.notify import notify_admin
from api.functions.execute import execute
from api.functions.exists import exists
from api.functions.log import logger


# Initate flask
app = Flask(__name__)

# Set CORS
CORS(app)


# ---------- Gods ----------

# Login God
@app.route('/api/auth/login', methods=['POST'])
@apiKey
def login_god():
    response = {}

    cursor, connection = database()

    username = request.json['username']
    password = request.json['password']

    cursor.execute(
        'SELECT * FROM USERS WHERE username = ? AND password = ? AND role = ?', (username, password, "god",))

    result = cursor.fetchall()
    connection.close()

    if len(result) > 0:
        user = {
            "id": result[0][0],
            "username": result[0][1],
            "password": result[0][2],
            "role": result[0][3],
            "name": result[0][6],
        }

        messages = ["Action: Login",
                    "Role: God", f"Username: {username}"]
        message = "\n".join(messages)

        log_data = {
            "action": "login",
            "level": 1,
            "role": "god",
            "username": username,
        }

        logger(log_data)

        notify_admin(message)

        response['message'] = "Welcome"
        response['user'] = user

        return jsonify(response), 200
    else:
        response['message'] = "Sorry, username or password is incorrect"

        return jsonify(response), 401


# Register God
@app.route('/api/auth/register', methods=['POST'])
@apiKey
def register_god():
    response = {}

    cursor, connection = database()

    username = request.json['username']
    password = request.json['password']
    chatid = request.json['chatid']
    name = request.json['name']

    count = exists(username)

    if count != 0:
        response['message'] = 'Username already exists'

        return jsonify(response), 400

    timestamp = datetime.datetime.now()

    cursor.execute(
        'INSERT INTO USERS (username, password, role, chatid, name, owner, timestamp) VALUES (?, ?, ?, ?, ?, timestamp)', (username, password, "god", chatid, name, "god", timestamp,))

    connection.commit()
    connection.close()

    messages = ["Action: Create", "Role: God", f"Username: {username}"]
    message = "\n".join(messages)

    log_data = {
        "action": "create",
        "level": 3,
        "role": "god",
        "username": username,
    }

    logger(log_data)

    notify_admin(message)

    response['message'] = "God created"

    return jsonify(response), 200


# All Gods
@app.route('/api/gods', methods=['GET'])
@apiKey
def all_gods():
    response = {}

    cursor, connection = database()

    cursor.execute("SELECT * FROM USERS WHERE role = ?", ("god",))
    execution = cursor.fetchall()

    users = []

    for record in execution:
        user = {
            "id": record[0],
            "username": record[1],
            "password": record[2],
            "role": record[3],
            "chatid": record[4],
            "name": record[6],
            "timestamp": record[7],
        }
        users.append(user)

    connection.close()

    response['data'] = users

    return jsonify(response), 200


# Update God
@app.route('/api/gods/<username>', methods=['PATCH'])
@apiKey
def update_god(username):
    response = {}

    body = request.json

    username = username.split('/')[-1]

    q = "UPDATE USERS SET "
    r = []

    for index, item in enumerate(body):
        if (len(body) == index + 1):
            q += f"{item} = ? "
            r.append(body[item])
        else:
            q += f"{item} = ?, "
            r.append(body[item])

    q += "WHERE username = ?"
    r.append(username)

    cursor, connection = database()

    cursor.execute(q, tuple(r))

    connection.commit()
    connection.close()

    response['message'] = "User updated"

    return jsonify(response), 404


# Delete God
@app.route('/api/gods/<username>', methods=['DELETE'])
@apiKey
def delete_god(username):
    response = {}

    username = username.split('/')[-1]

    cursor, connection = database()

    cursor.execute(
        'DELETE FROM USERS WHERE username = ?', (username,))

    connection.commit()
    connection.close()

    messages = ["Action: Delete", "Role: God", f"Username: {username}"]
    message = "\n".join(messages)

    log_data = {
        "action": "delete",
        "level": 2,
        "role": "god",
        "username": username,
    }

    logger(log_data)

    notify_admin(message)

    response['message'] = "User deleted"

    return jsonify(response), 200


# ---------- Admins ----------


# Login Admin
@app.route('/api/admins/login', methods=['POST'])
@apiKey
def login_admin():
    response = {}

    cursor, connection = database()

    username = request.json['username']
    password = request.json['password']

    cursor.execute(
        'SELECT * FROM USERS WHERE username = ? AND password = ? AND role = ?', (username, password, "admin",))

    result = cursor.fetchall()
    connection.close()

    if len(result) > 0:
        user = {
            "id": result[0][0],
            "username": result[0][1],
            "password": result[0][2],
            "role": result[0][3],
            "name": result[0][6],
        }

        messages = ["Action: Login",
                    "Role: Admin", f"Username: {username}"]
        message = "\n".join(messages)

        log_data = {
            "action": "login",
            "level": 1,
            "role": "admin",
            "username": username,
        }

        logger(log_data)

        notify_admin(message)

        response['message'] = "Welcome"
        response['user'] = user

        return jsonify(response), 200
    else:
        response['message'] = "Sorry, username or password is incorrect"

        return jsonify(response), 401


# Register Admin
@app.route('/api/admins/register', methods=['POST'])
@apiKey
def register_admin():
    response = {}

    cursor, connection = database()

    username = request.json['username']
    password = request.json['password']
    name = request.json['name']
    owner = request.json['owner']

    count = exists(username)

    if count != 0:
        response['message'] = 'Username already exists'

        return jsonify(response), 400

    script_path = os.path.join(path, 'scripts/crud/create.sh')
    execution = execute(script_path, username, password)

    timestamp = datetime.datetime.now()

    if execution:
        cursor.execute(
            'INSERT INTO USERS (username, password, role, name, owner, timestamp) VALUES (?, ?, ?, ?, ?)', (username, password, "admin", name, owner, timestamp,))

        connection.commit()
        connection.close()

        messages = ["Action: Create",
                    "Role: Admin", f"Username: {username}"]
        message = "\n".join(messages)

        log_data = {
            "action": "create",
            "level": 3,
            "role": "admin",
            "username": username,
        }

        logger(log_data)

        notify_admin(message)

        response['message'] = "Admin created"

        return jsonify(response), 200
    else:
        response['message'] = 'Sorry, an error!'

        return jsonify(response), 500


# All Admins
@app.route('/api/admins', methods=['GET'])
@apiKey
def all_admins():
    response = {}

    cursor, connection = database()

    cursor.execute("SELECT * FROM USERS WHERE role = ?", ("admin",))
    execution = cursor.fetchall()

    users = []

    for record in execution:
        user = {
            "id": record[0],
            "username": record[1],
            "password": record[2],
            "role": record[3],
            "name": record[6],
            "timestamp": record[7],
        }
        users.append(user)

    connection.close()

    response['data'] = users

    return jsonify(response), 200


# Update Admin
@app.route('/api/admins/<username>', methods=['PATCH'])
@apiKey
def update_admin(username):
    response = {}

    body = request.json

    username = username.split('/')[-1]

    q = "UPDATE USERS SET "
    r = []

    for index, item in enumerate(body):
        if (len(body) == index + 1):
            q += f"{item} = ? "
            r.append(body[item])
        else:
            q += f"{item} = ?, "
            r.append(body[item])

    q += "WHERE username = ?"
    r.append(username)

    cursor, connection = database()

    cursor.execute(q, tuple(r))

    connection.commit()
    connection.close()

    response['message'] = "User updated"

    return jsonify(response), 404


# Delete Admin
@app.route('/api/admins/<username>', methods=['DELETE'])
@apiKey
def delete_admin(username):
    response = {}

    username = username.split('/')[-1]

    cursor, connection = database()

    cursor.execute(
        'DELETE FROM USERS WHERE username = ?', (username,))

    connection.commit()
    connection.close()

    messages = ["Action: Delete", "Role: Admin", f"Username: {username}"]
    message = "\n".join(messages)

    log_data = {
        "action": "delete",
        "level": 2,
        "role": "admin",
        "username": username,
    }

    logger(log_data)

    notify_admin(message)

    response['message'] = "User deleted"

    return jsonify(response), 200


# ---------- Clients ----------


# All Clients
@app.route('/api/clients', methods=['GET'])
@apiKey
def all_users():
    response = {}

    cursor, connection = database()

    cursor.execute("SELECT * FROM USERS WHERE role = ?", ("client",))
    execution = cursor.fetchall()

    users = []

    for record in execution:
        user = {
            "id": record[0],
            "username": record[1],
            "password": record[2],
            "role": record[3],
            "owner": record[5],
            "name": record[6],
            "timestamp": record[7],
            "expire": record[8],
            "access": record[9]
        }
        users.append(user)

    connection.close()

    response['data'] = users

    return jsonify(response), 200


# All Clients Filter For Owner
@app.route('/api/clients/<owner>', methods=['GET'])
@apiKey
def all_for_owner(owner):
    response = {}

    cursor, connection = database()

    cursor.execute(
        "SELECT * FROM USERS WHERE role = ? AND owner = ?", ("client", owner,))
    execution = cursor.fetchall()

    users = []

    for record in execution:
        user = {
            "id": record[0],
            "username": record[1],
            "password": record[2],
            "role": record[3],
            "name": record[6],
            "timestamp": record[7],
            "expire": record[8],
            "access": record[9]
        }
        users.append(user)

    connection.close()

    response['data'] = users

    return jsonify(response), 200


# Create Client
@app.route('/api/clients', methods=['POST'])
@apiKey
def create_client():
    response = {}

    cursor, connection = database()

    username = request.json['username']
    password = request.json['password']
    owner = request.json['owner']
    name = request.json['name']
    expire = request.json['expire']

    count = exists(username)

    if count != 0:
        response['message'] = 'Username already exists'

        return jsonify(response), 400

    script_path = os.path.join(path, 'scripts/crud/create.sh')
    execution = execute(script_path, username, password)

    timestamp = datetime.datetime.now()
    expire = timestamp + datetime.timedelta(days=int(expire))

    if execution:
        cursor.execute(
            'INSERT INTO USERS (username, password, role, owner, name, timestamp, expire, access) VALUES (?, ?, ?, ?, ?, ?, ?, ?)',
            (username, password, "client", owner, name, timestamp, expire, True)
        )

        connection.commit()
        connection.close()

        messages = ["Action: Create", "Role: Client",
                    f"Username: {username}", f"Creator: {owner}"]
        message = "\n".join(messages)

        log_data = {
            "action": "create",
            "level": 3,
            "role": "client",
            "creator": owner,
            "username": username,
        }

        logger(log_data)

        notify_admin(message)

        response['message'] = "Client created"

        return jsonify(response), 200
    else:
        response['message'] = 'Sorry, an error!'

        return jsonify(response), 500


# Update Client
@app.route('/api/clients/<username>', methods=['PATCH'])
@apiKey
def update_client(username):
    response = {}

    body = request.json

    username = username.split('/')[-1]

    q = "UPDATE USERS SET "
    r = []

    for index, item in enumerate(body):
        if (len(body) == index + 1):
            q += f"{item} = ? "
            r.append(body[item])
        else:
            q += f"{item} = ?, "
            r.append(body[item])

    q += "WHERE username = ?"
    r.append(username)

    cursor, connection = database()

    cursor.execute(q, tuple(r))

    connection.commit()
    connection.close()

    response['message'] = "User updated"

    return jsonify(response), 200


# Update Client Access
@app.route('/api/clients/access/<username>', methods=['PATCH'])
@apiKey
def update_client_access(username):
    response = {}

    access = request.json["access"]

    username = username.split('/')[-1]

    cursor, connection = database()

    cursor.execute("UPDATE USERS SET access = ? WHERE username = ?", (access, username,))

    connection.commit()
    connection.close()

    response['message'] = "User access updated"

    return jsonify(response), 200


# Delete Client
@app.route('/api/clients/<username>', methods=['DELETE'])
@apiKey
def delete_client(username):
    response = {}

    username = username.split('/')[-1]

    cursor, connection = database()

    script_path = os.path.join(path, 'scripts/crud/delete.sh')
    execution = execute(script_path, username)

    if execution:
        cursor.execute(
            'DELETE FROM USERS WHERE username = ?', (username,))

        connection.commit()
        connection.close()

        messages = ["Action: Delete",
                    "Role: Client", f"Username: {username}"]
        message = "\n".join(messages)

        log_data = {
            "action": "delete",
            "level": 2,
            "role": "client",
            "username": username,
        }

        logger(log_data)

        notify_admin(message)

        response['message'] = "User deleted"

        return jsonify(response), 200
    else:
        response['message'] = 'Sorry, an error!'

        return jsonify(response), 500


# ---------- Users ----------


# Add Users
@app.route('/api/v', methods=['GET'])
@apiKey
def read():
    response = {}

    cursor, connection = database()

    cursor.execute("SELECT * FROM USERS")
    execution = cursor.fetchall()

    users = []

    for record in execution:
        user = {
            "id": record[0],
            "username": record[1],
            "password": record[2],
            "role": record[3],
            "chatid": record[4],
            "owner": record[5],
            "name": record[6],
            "timestamp": record[7],
            "expire": record[8],
            "access": record[9],
        }
        users.append(user)

    connection.close()

    response['data'] = users

    return jsonify(response), 200


# Create
@app.route('/api/v', methods=['POST'])
@apiKey
def create():
    response = {}

    body = request.json

    days_ago = datetime.datetime.now() - datetime.timedelta(days=31)

    q = "INSERT INTO USERS ("
    columns = []
    placeholders = []
    r = []

    for item in body:
        columns.append(item)
        placeholders.append('?')
        r.append(body[item])

    columns.append("timestamp")
    placeholders.append('?')
    r.append(days_ago)

    q += ', '.join(columns) + ") VALUES (" + ', '.join(placeholders) + ")"

    cursor, connection = database()

    cursor.execute(q, tuple(r))

    connection.commit()
    connection.close()

    response['message'] = "User created"

    return jsonify(response), 201


# Update User
@app.route('/api/v/<id>', methods=['PATCH'])
@apiKey
def update(id):
    response = {}

    body = request.json

    q = "UPDATE USERS SET "
    r = []

    for index, item in enumerate(body):
        if (len(body) == index + 1):
            q += f"{item} = ? "
            r.append(body[item])
        else:
            q += f"{item} = ?, "
            r.append(body[item])

    q += "WHERE id = ?"
    r.append(id)

    cursor, connection = database()

    cursor.execute(q, tuple(r))

    connection.commit()
    connection.close()

    response['message'] = "User updated"

    return jsonify(response), 404


# Delete User
@app.route('/api/v/<id>', methods=['DELETE'])
@apiKey
def delete(id):
    response = {}

    cursor, connection = database()

    cursor.execute(
        'DELETE FROM USERS WHERE id = ?', (id,))

    connection.commit()
    connection.close()

    response['message'] = "User deleted"

    return jsonify(response), 200


# ---------- Logs ----------


# All logs
@app.route('/api/logs', methods=['GET'])
@apiKey
def logs():
    response = {}

    cursor, connection = database()

    q = "SELECT * FROM LOGS"
    r = []

    logs = []

    if len(request.args) > 0:
        for index, item in enumerate(request.args.items()):
            if index == 0:
                q += " WHERE "

            if (len(request.args) == index + 1):
                q += f"{item[0]} = ? "
                r.append(item[1])
            else:
                q += f"{item[0]} = ?, "
                r.append(item[1])

    cursor.execute(q, tuple(r))

    result = cursor.fetchall()
    connection.close()

    for record in result:
        log = {
            "_id": record[0],
            "username": record[1],
            "action": record[2],
            "role": record[3],
            "level": record[4],
            "creator":  record[5],
        }

        logs.append(log)

    response['data'] = logs

    return jsonify(response), 200


# ---------- Migration ----------

# Migrate from db to kernel
@app.route('/api/migration', methods=['GET'])
@apiKey
def migration():
    response = {}

    cursor, connection = database()

    cursor.execute("SELECT * FROM USERS WHERE role IS NOT 'god'")

    users = [{'username': i[1], 'password': i[2]} for i in cursor.fetchall()]

    for user in users:
        script_path = os.path.join(path, 'scripts/crud/create.sh')
        execution = execute(script_path, user['username'], user['password'])

        if execution:
            user['executed'] = True
        else:
            user['executed'] = False

    response['data'] = users

    connection.close()

    return jsonify(response), 200


# ---------- Expire ----------

# Delete expired
@app.route('/api/expired', methods=['GET'])
@apiKey
def expired():
    response = {}

    cursor, connection = database()

    current = datetime.datetime.now()

    cursor.execute(
        'SELECT * FROM USERS WHERE role = "client" AND expire <= ?', (current,))
    results = cursor.fetchall()

    connection.close()

    users = []
    messages = ["Action: Delete expireds", "Role: System", "Deleted users:"]

    for record in results:
        cursor_l, connection_l = database()

        user = {
            "id": record[0],
            "username": record[1],
            "password": record[2],
            "role": record[3],
            "owner": record[5],
            "name": record[6],
            "timestamp": record[7],
            "expire": record[8],
            "access": record[9]
        }

        script_path = os.path.join(path, 'scripts/crud/delete.sh')
        execution = execute(script_path, record[1])

        if execution:
            cursor_l.execute(
                'DELETE FROM USERS WHERE username = ?', (record[1],))

            connection_l.commit()
            connection_l.close()

            messages.append(f'{record[1]} by {record[5]} ✅')
            user['executed'] = True
        else:
            messages.append(f'{record[1]} by {record[5]} ❌')
            user['executed'] = False

        users.append(user)

    message = "\n".join(messages)

    notify_admin(message)

    response['data'] = users

    return jsonify(response), 200
