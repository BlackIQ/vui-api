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


# ---------- Admins ----------

# Login God
@app.route('/api/auth/login', methods=['POST'])
@apiKey
def login_god():
    response = {}

    cursor, connection = database()

    username = request.json['username']
    password = request.json['password']

    cursor.execute(
        'SELECT * FROM GODS WHERE username = ? AND password = ?', (username, password,))

    result = cursor.fetchall()
    connection.close()

    if len(result) > 0:
        user = {
            "id": result[0][0],
            "username": result[0][1],
            "password": result[0][2],
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

    cursor.execute(
        'INSERT INTO GODS (username, password) VALUES (?, ?)', (username, password,))

    connection.commit()
    connection.close()

    messages = ["New user", "\n", "Role: God", f"Username: {username}"]
    message = "\n".join(messages)

    send(message, 6079800600)

    response['message'] = "God created"

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
        'SELECT * FROM USERS WHERE username = ? AND password = ? AND isAdmin = true', (username, password,))

    result = cursor.fetchall()
    connection.close()

    if len(result) > 0:
        user = {
            "id": result[0][0],
            "username": result[0][1],
            "password": result[0][2],
            "isAdmin": result[0][3]
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

    cursor.execute(
        'INSERT INTO USERS (username, password, isAdmin) VALUES (?, ?, ?)', (username, password, True,))

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
def add_admins():
    response = {}

    cursor, connection = database()

    cursor.execute("SELECT * FROM USERS WHERE isAdmin = 1")
    execution = cursor.fetchall()

    users = []

    for record in execution:
        user = {
            "id": record[0],
            "username": record[1],
            "password": record[2],
        }
        users.append(user)

    connection.close()

    response['data'] = users

    return jsonify(response), 200


# ---------- Clients ----------


# All Clients Filter For Owner
@app.route('/api/clients', methods=['GET'])
@apiKey
def all_users():
    response = {}

    cursor, connection = database()

    cursor.execute("SELECT * FROM USERS WHERE isAdmin = 0")
    execution = cursor.fetchall()

    users = []

    for record in execution:
        user = {
            "id": record[0],
            "username": record[1],
            "password": record[2],
            "isAdmin": record[3]
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

    cursor.execute("SELECT * FROM USERS WHERE owner = ?", (owner,))
    execution = cursor.fetchall()

    users = []

    for record in execution:
        user = {
            "id": record[0],
            "username": record[1],
            "password": record[2],
            "isAdmin": record[3]
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

    script_path = os.path.join(path, 'scripts/create.sh')
    execution = execute(script_path, username, password)

    if execution:
        cursor.execute(
            'INSERT INTO USERS (username, password, isAdmin, owner) VALUES (?, ?, ?, ?)', (username, password, False, owner,))

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
def update_client(id):
    response = {}

    response['message'] = "User updating is not available"

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
