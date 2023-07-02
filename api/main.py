from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)


@app.route('/api/predict', methods=['GET'])
def predict():
    response = {'message': 'ok'}

    return jsonify(response)
