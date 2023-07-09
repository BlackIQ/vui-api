# Flask
from flask import Flask, request, jsonify
from flask_cors import CORS

# Python libs
import os


# Middlewares
from api.middlewares.apikey import apiKey

# Config
from api.config.config import path

# Database
from api.database.sqlite import database

# Functions
from api.functions.execute import execute
from api.functions.message import send

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
        }

        messages = ["New login", "\n", "Role: God", f"Username: {username}"]
        message = "\n".join(messages)

        send(message, 6079800600)

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

    cursor.execute(
        'INSERT INTO USERS (username, password, role, chatid, name) VALUES (?, ?, ?, ?, ?)', (username, password, "god", chatid, name,))

    connection.commit()
    connection.close()

    messages = ["New user", "\n", "Role: God", f"Username: {username}"]
    message = "\n".join(messages)

    send(message, 6079800600)

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
        print(record)

        user = {
            "id": record[0],
            "username": record[1],
            "password": record[2],
            "role": record[3],
            "chatid": record[4],
            "name": record[6],
        }
        users.append(user)

    connection.close()

    response['data'] = users

    return jsonify(response), 200


# Update Client
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


# Delete Client
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

    messages = ["Delete user", "\n",
                "Role: God", f"Username: {username}"]
    message = "\n".join(messages)

    send(message, 6079800600)

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
            "role": result[0][3]
        }

        messages = ["New login", "\n", "Role: Admin", f"Username: {username}"]
        message = "\n".join(messages)

        send(message, 6079800600)

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

    cursor.execute(
        'INSERT INTO USERS (username, password, role, name) VALUES (?, ?, ?, ?)', (username, password, "admin", name,))

    connection.commit()
    connection.close()

    messages = ["New user", "\n", "Role: Admin", f"Username: {username}"]
    message = "\n".join(messages)

    send(message, 6079800600)

    response['message'] = "Admin created"

    return jsonify(response), 200


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
        }
        users.append(user)

    connection.close()

    response['data'] = users

    return jsonify(response), 200


# Update Client
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


# Delete Client
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

    messages = ["Delete user", "\n",
                "Role: Admin", f"Username: {username}"]
    message = "\n".join(messages)

    send(message, 6079800600)

    response['message'] = "User deleted"

    return jsonify(response), 200


# ---------- Clients ----------


# All Clients Filter For Owner
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

    script_path = os.path.join(path, 'scripts/create.sh')
    execution = execute(script_path, username, password)

    if execution:
        cursor.execute(
            'INSERT INTO USERS (username, password, role, owner, name) VALUES (?, ?, ?, ?, ?)', (username, password, "client", owner, name,))

        connection.commit()
        connection.close()

        messages = ["New user", "\n", "Role: Client",
                    f"Username: {username}", f"Creator: {owner}"]
        message = "\n".join(messages)

        send(message, 6079800600)

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

    return jsonify(response), 404


# Delete Client
@app.route('/api/clients/<username>', methods=['DELETE'])
@apiKey
def delete_client(username):
    response = {}

    username = username.split('/')[-1]

    cursor, connection = database()

    script_path = os.path.join(path, 'scripts/delete.sh')
    execution = execute(script_path, username)

    if execution:
        cursor.execute(
            'DELETE FROM USERS WHERE username = ?', (username,))

        connection.commit()
        connection.close()

        messages = ["Delete user", "\n",
                    "Role: Client", f"Username: {username}"]
        message = "\n".join(messages)

        send(message, 6079800600)

        response['message'] = "User deleted"

        return jsonify(response), 200
    else:
        response['message'] = 'Sorry, an error!'

        return jsonify(response), 500
