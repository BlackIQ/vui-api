from flask import Flask, request, jsonify
from flask_cors import CORS

from functools import wraps
import os


from api.config.config import path, env
from api.database.sqlite import database
from api.functions.execute import execute

app = Flask(__name__)
CORS(app)


def apiKey(func):
    @wraps(func)
    def decorated_function(*args, **kwargs):
        api_key = request.headers.get('apiKey')

        if api_key and api_key == env["API_KEY"]:
            return func(*args, **kwargs)
        else:
            return jsonify({'message': 'Unauthorized'}), 401

    return decorated_function


@app.route('/api/auth/login', methods=['POST'])
def login_user():
    response = {}

    cursor, connection = database()

    username = request.json['username']
    password = request.json['password']

    cursor.execute(
        'SELECT * FROM USERS WHERE username = ? AND password = ? AND isAdmin = true', (username, password,))

    result = cursor.fetchall()

    connection.close()

    if len(result) > 0:
        response['message'] = "Welcome"

        return jsonify(response), 200
    else:
        response['message'] = "Sorry, username or password is incorrect"

        return jsonify(response), 401


@app.route('/api/users', methods=['GET'])
@apiKey
def all_users():
    response = {}

    cursor, connection = database()

    cursor.execute("SELECT * FROM USERS")
    execution = cursor.fetchall()

    cursor.execute(
        "SELECT COUNT(*) AS cAll, \
        SUM(CASE WHEN isAdmin = 1 THEN 1 ELSE 0 END) AS cAdmin, \
        SUM(CASE WHEN isAdmin = 0 THEN 1 ELSE 0 END) AS cUsers \
        FROM USERS"
    )

    result = cursor.fetchone()

    cAll = result[0]
    cAdmins = result[1]
    cUsers = result[2]

    count = {
        "total": cAll,
        "users": 0 if cUsers == None else cUsers,
        "admins": 0 if cAdmins == None else cAdmins,
    }

    response['count'] = count

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


@app.route('/api/users', methods=['POST'])
@apiKey
def create_user():
    response = {}

    cursor, connection = database()

    username = request.json['username']
    password = request.json['password']
    isAdmin = request.json['isAdmin']

    if isAdmin == False:
        script_path = os.path.join(path, 'scripts/create.sh')
        execution = execute(script_path, username, password)

        if execution:

            cursor.execute(
                'INSERT INTO USERS (username, password, isAdmin) VALUES (?, ?, ?)', (username, password, isAdmin,))

            connection.commit()
            connection.close()

            response['message'] = "User created"

            return jsonify(response), 200
        else:
            response['message'] = 'Sorry, an error!'

        return jsonify(response), 500
    else:
        cursor.execute(
            'INSERT INTO USERS (username, password, isAdmin) VALUES (?, ?, ?)', (username, password, isAdmin,))

        connection.commit()
        connection.close()

        response['message'] = "Admin created"

        return jsonify(response), 200


@app.route('/api/users/<username>', methods=['PATCH'])
@apiKey
def update_user(id):
    response = {}

    response['message'] = "User updating is not available"

    return jsonify(response), 404


@app.route('/api/users/<username>', methods=['DELETE'])
@apiKey
def delete_user(username):
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

        response['message'] = "User deleted"

        return jsonify(response), 200
    else:
        response['message'] = 'Sorry, an error!'

        return jsonify(response), 500
