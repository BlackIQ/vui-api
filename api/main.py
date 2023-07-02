from flask import Flask, request, jsonify
from flask_cors import CORS


from api.config.config import path
from api.database.sqlite import database
from api.functions.execute import execute

app = Flask(__name__)
CORS(app)


@app.route('/api/users', methods=['GET'])
def all_users():
    cursor, connection = database()

    cursor.execute("SELECT * FROM User")
    users = cursor.fetchall()

    connection.close()

    return jsonify(users), 200

    # script_path = os.path.join(path, 'scripts\\test.sh')
    # execution = execute(script_path, "amir")

    # status_code = 0

    # if execution:
    #     status_code = 200
    #     response['status'] = 'success'
    # else:
    #     status_code = 500
    #     response['status'] = 'error'

    # return jsonify(response), status_code


@app.route('/api/users', methods=['POST'])
def create_user():
    cursor, connection = database()

    response = {}
    status_code = 0

    username = request.json['username']
    password = request.json['password']

    cursor.execute(
        'INSERT INTO User (username, password) VALUES (?, ?)', (username, password))
    connection.commit()
    connection.close()

    response['message'] = "User created"
    status_code = 200

    return jsonify(response), status_code


@app.route('/api/users/<id>', methods=['PATCH'])
def update_user(id):
    cursor, connection = database()

    response = {}

    try:
        cursor.execute("SELECT * FROM User WHERE id = ?", (id))

        if (len(cursor.fetchall()) > 0):
            print("Yes")
        else:
            raise Exception({'message': 'User not found', 'status_code': 404})

        try:
            username = request.json['username']
            password = request.json['password']

            cursor.execute(
                'UPDATE User SET username = ?, password = ? WHERE id = ?', (username, password, id))
            connection.commit()

            response['message'] = "User updated"

            return jsonify(response), 200
        except Exception as e:
            response['message'] = e

            return jsonify(response), 500
        finally:
            connection.close()
    except Exception as e:
        response['message'] = str(e)

        return jsonify(response), 404
    finally:
        connection.close()


@app.route('/api/users/<id>', methods=['DELETE'])
def delete_user(id):
    cursor, connection = database()

    response = {}
    status_code = 0

    cursor.execute(
        'DELETE FROM User WHERE id = ?', (id))
    connection.commit()
    connection.close()

    response['message'] = "User deleted"
    status_code = 200

    return jsonify(response), status_code
