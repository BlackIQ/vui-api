# Flask
from flask import Flask, request, jsonify
from flask_cors import CORS

# Python libs
import os

# Database
from api.database.sqlite import database

# Middlewares
from api.middlewares.apikey import apiKey

# Config
from api.config.config import path
from api.config.db import SECRET

# Functions
from api.functions.execute import execute
from api.functions.exists import exists


# Initate flask
app = Flask(__name__)

# Set CORS
CORS(app)

PRODUCTION = False


# ---------- Authentication ----------

# Login
@app.route(f'/{SECRET}/api/auth/login', methods=['POST'])
@apiKey
def login():
    response = {}

    cursor, connection = database()

    username = request.json['username']
    password = request.json['password']
    
    cursor.execute(
        'SELECT * FROM USERS WHERE username = ? AND password = ?', (username, password))

    result = cursor.fetchall()
    connection.close()

    if len(result) > 0:
        user = {
            "id": result[0][0],
            "username": result[0][1],
            "password": result[0][2],
        }
        
        response['message'] = "Welcome"
        response['user'] = user

        return jsonify(response), 200
    else:
        response['message'] = "Sorry, username or password is incorrect"

        return jsonify(response), 401

# ---------- Clients ----------


# All Clients
@app.route(f'/{SECRET}/api/clients/all', methods=['GET'])
@apiKey
def all_clients():
    response = {}

    cursor, connection = database()

    cursor.execute("SELECT * FROM CLIENTS")
    execution = cursor.fetchall()

    clients = []

    for record in execution:
        cleint = {
            "id": record[0],
            "name": record[1],
            "username": record[2],
            "password": record[3],
            "access": record[4]
        }
        clients.append(cleint)

    connection.close()

    response['data'] = clients

    return jsonify(response), 200


# Create Client
@app.route(f'/{SECRET}/api/clients/create', methods=['POST'])
@apiKey
def create_client():
    response = {}

    cursor, connection = database()

    username = request.json['username']
    password = request.json['password']
    name = request.json['name']

    count = exists(username)

    if count != 0:
        response['message'] = 'Username already exists'

        return jsonify(response), 400

    if PRODUCTION:
        script_path = os.path.join(path, 'scripts/crud/create.sh')
        execution = execute(script_path, username, password)
    else:
        execution = True

    if execution:
        cursor.execute(
            'INSERT INTO CLIENTS (name, username, password, access) VALUES (?, ?, ?, ?)',
            (name, username, password, True)
        )

        connection.commit()
        connection.close()

        response['message'] = "Client created"

        return jsonify(response), 200
    else:
        response['message'] = 'Sorry, an error!'

        return jsonify(response), 500


# Update Client
@app.route(f'/{SECRET}/api/clients/update/<username>', methods=['PATCH'])
@apiKey
def update_client(username):
    response = {}

    body = request.json

    username = username.split('/')[-1]
    
    count = exists(username)

    if count == 0:
        response['message'] = 'Username is not exists'

        return jsonify(response), 400

    q = "UPDATE CLIENTS SET "
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
@app.route(f'/{SECRET}/api/clients/access/<username>', methods=['PATCH'])
@apiKey
def update_client_access(username):
    response = {}

    access = request.json["access"]

    username = username.split('/')[-1]
    
    count = exists(username)

    if count == 0:
        response['message'] = 'Username is not exists'

        return jsonify(response), 400

    file = ""

    if (access):
        file = "enable"
    else:
        file = "disable"

    if PRODUCTION:
        script_path = os.path.join(path, f'scripts/access/{file}.sh')
        execution = execute(script_path, username)
    else:
        execution = True

    if execution:
        cursor, connection = database()

        cursor.execute("UPDATE CLIENTS SET access = ? WHERE username = ?", (access, username,))

        connection.commit()
        connection.close()

        response['message'] = "User access updated"

        return jsonify(response), 200
    else:
        response['message'] = 'Sorry, an error!'

        return jsonify(response), 500


# Delete Client
@app.route(f'/{SECRET}/api/clients/delete/<username>', methods=['DELETE'])
@apiKey
def delete_client(username):
    response = {}

    username = username.split('/')[-1]
        
    count = exists(username)

    if count == 0:
        response['message'] = 'Username is not exists'

        return jsonify(response), 400

    cursor, connection = database()

    if PRODUCTION:
        script_path = os.path.join(path, 'scripts/crud/delete.sh')
        execution = execute(script_path, username)
    else:
        execution = True

    if execution:
        cursor.execute(
            'DELETE FROM CLIENTS WHERE username = ?', (username,))

        connection.commit()
        connection.close()

        response['message'] = "User deleted"

        return jsonify(response), 200
    else:
        response['message'] = 'Sorry, an error!'

        return jsonify(response), 500