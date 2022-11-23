#!/usr/bin/env python3
import json
import signal
import os
from flask import Flask, jsonify, request


app = Flask(__name__)

mock_data = {}


@app.route('/', methods=['GET'])
def mock_root():
    return {"This is": "mock"}


@app.route('/add_person', methods=['POST'])
def create_person_mock():
    person_name = json.loads(request.data)["name"]
    if person_name not in mock_data:
        mock_data[person_name] = {"job": json.loads(request.data)["job"],
                                  "person_id": json.loads(request.data)["person_id"]}
        return jsonify(f'Person with id {mock_data[person_name]["person_id"]} created'), 201
    else:
        return jsonify(f'{person_name} is not existing'), 400


@app.route('/get_person_id/<name>', methods=['GET'])
def get_person_id_mock(name):
    if name in mock_data:
        return jsonify(mock_data[name]["person_id"]), 200
    else:
        return jsonify(f'Person {name} is not created'), 400


@app.route('/persons/<name>', methods=['PUT'])
def update_person_mock(name):
    person_name = json.loads(request.data)["name"]
    if person_name in mock_data:
        mock_data[person_name]["job"] = json.loads(request.data)["job"]
        return jsonify(f'Person updated. Person job now is {mock_data[person_name]["job"]}'), 201
    else:
        return jsonify(f'Person {person_name} is not existing'), 400


@app.route('/persons/<name>', methods=['DELETE'])
def delete_person_mock(name):
    if name in mock_data:
        mock_data.pop(name)
        return jsonify(f'Person {name} deleted'), 200
    else:
        return jsonify(f'Person {name} is not existing'), 400


@app.route('/shutdown')
def shutdown_mock():
    os.kill(os.getpid(), signal.SIGINT)
    return jsonify('Mock is shutting down')


if __name__ == "__main__":
    app.run(host='127.0.0.1', port=8082)
