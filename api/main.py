from flask import Flask, request, jsonify
from flask_cors import CORS

from api.config.config import path

app = Flask(__name__)
CORS(app)


@app.route('/api/users', methods=['GET'])
def all_users():
    response = {'message': 'read', 'path': path}

    return jsonify(response)


@app.route('/api/users', methods=['POST'])
def create_user():
    response = {'message': 'create'}

    username = request.json['username']
    password = request.json['password']

    print(username, password)

    return jsonify(response)


@app.route('/api/users/<username>', methods=['PATCH'])
def update_user(username):
    response = {'message': 'update'}

    print(username)

    return jsonify(response)


@app.route('/api/users/<username>', methods=['DELETE'])
def delete_user(username):
    response = {'message': 'delete'}

    print(username)

    return jsonify(response)
