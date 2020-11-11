"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db,User, Task


app = Flask(__name__)
app.url_map.strict_slashes = False
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DB_CONNECTION_STRING')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)


@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code


@app.route('/')
def sitemap():
    return generate_sitemap(app)


@app.route('/user', methods=['GET'])
def handle_hello():
    response_body = {
        "msg": "Hello, this is your GET /user response "
    }
    return jsonify(response_body), 200


@app.route('/todos/<username>', methods=['GET'])
def get_todos(username):
    tasks = Task.get_task_by_username(username)
    return jsonify({
        "message":f"These are the tasks available for user {username}",
        "task":tasks
    }), 200


@app.route('/todos/<username>', methods=['POST'])
def create_todos(username):
    request_data= request.get_json()
    task=Task(request_data["label"],request_data["done"],username)
    task.save_to_data()
    return jsonify({"Message":"Task created" })

@app.route('/todos/<id>', methods=['PUT'])
def update_todos(id):
    task= Task.get_task_by_id(int(id))
    request_data=request.get_json()
    task.label=request_data["label"]
    task.done=request_data["done"]
    task.save_to_data()
    return jsonify({
        "Message":"Task updated",
        "Task_updater":task.serialize()
    })

@app.route('/todos/<id>', methods=['DELETE'])
def delete_todos(id):
    task=Task.get_task_by_id(int(id))
    if task is None: 
        raise APIException("Id not found ", 404)
    task.delete_from_database()
    return jsonify({"Message":"Task deleted"})

# this only runs if `$ python src/main.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
