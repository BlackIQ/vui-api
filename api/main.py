from flask import Flask, request, jsonify
from flask_cors import CORS

import os


from api.config.config import path
from api.database.sqlite import database
from api.functions.execute import execute

app = Flask(__name__)
CORS(app)


@app.route('/api/users', methods=['GET'])
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
        "users": cUsers,
        "admins": cAdmins
    }

    response['count'] = count

    users = []

    for record in execution:
        user = {
            "id": record[0],
            "name": record[1],
            "password": record[2],
            "isAdmin": record[3]
        }
        users.append(user)

    connection.close()

    response['data'] = users

    return jsonify(response), 200


@ app.route('/api/users', methods=['POST'])
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
                'INSERT INTO USERS (username, password, isAdmin) VALUES (?, ?, ?)', (username, password, isAdmin))

            connection.commit()
            connection.close()

            response['message'] = "User created"

            return jsonify(response), 200
        else:
            response['message'] = 'Sorry, an error!'

        return jsonify(response), 500
    else:
        response['message'] = "Admin created"

        return jsonify(response), 200


@ app.route('/api/users/<username>', methods=['PATCH'])
def update_user(id):
    response = {}

    response['message'] = "User updating is not available"

    return jsonify(response), 404


@ app.route('/api/users/<username>', methods=['DELETE'])
def delete_user(username):
    response = {}

    cursor, connection = database()

    script_path = os.path.join(path, 'scripts/delete.sh')
    execution = execute(script_path, username)

    if execution:
        cursor.execute(
            'DELETE FROM USERS WHERE username = ?', (username))

        connection.commit()
        connection.close()

        response['message'] = "User deleted"

        return jsonify(response), 200
    else:
        response['message'] = 'Sorry, an error!'

        return jsonify(response), 500
