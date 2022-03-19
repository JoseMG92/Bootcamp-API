import re
import utils
from flask import Flask, jsonify, request

PATH_BASE_API = "/api/v1"
app = Flask(__name__)

@app.route(f'{PATH_BASE_API}/')
def index():
    data = {
        "code": 200,

        "msg":"Online"
    }
    return jsonify(data)

@app.route(f'{PATH_BASE_API}/create-tables')
def create_tables():
    msg = utils.create_tables()
    resp = {"msg": msg}
    return resp

@app.route(f'{PATH_BASE_API}/user/create', methods = ['GET', 'POST'])
def create_user():
    if request.method == "POST":
        data = request.json
        first_name = data['first_name']
        last_name = data['last_name']
        email = data['email']
        password = data['password']
        confirm_password = data['confirm_password']
        msg = utils.db_create_user(first_name, last_name, email, password, confirm_password)
    elif request.method == 'GET':
        msg = 'Este endpoint es para registrar usuarios'
    return {
        "code": 200,
        "msg": msg,
    }

@app.route(f"{PATH_BASE_API}/user/<id_user>", methods = ['GET'])
def get_user(id_user):
    msg = utils.db_get_user(id_user)
    return msg

@app.route(f"{PATH_BASE_API}/user/delete/<id_user>", methods = ['DELETE'])
def delete_user(id_user):
    msg = utils.db_delete_user(id_user)
    return msg

@app.route(f"{PATH_BASE_API}/user/update/<id_user>", methods = ['PUT'])
def update_user(id_user):
    msg = utils.db_update_user(id_user)
    return msg

#Trabajo con tabla tasks
@app.route(f"{PATH_BASE_API}/tasks/create/<id_user>", methods = ['GET','POST'])
def create_task(id_user):
    if request.method == 'POST':
        data = request.json
        title = data['title']
        description = data['description']
        is_completed = data['is_completed']
        msg = utils.db_create_task(title,description,is_completed,id_user)
    elif request.method == 'GET':
        msg = 'Este endpoint es para crear una nueva tarea'
    return {
        "code":200,
        "msg": msg
    }

@app.route(f"{PATH_BASE_API}/tasks/user/<id_user>", methods = ['GET', 'POST'])
def get_tasks(id_user):
    if request.method == 'GET':
        msg = utils.db_get_task(id_user)
    elif request.method == 'POST':
        msg = 'Este endpoint es para consultar las tareas de un usuario'
    return {
        "code":200,
        "msg":msg
    }

@app.route(f"{PATH_BASE_API}/tasks/update/<id_task>", methods = ['PUT'])
def update_task(id_task):
    msg = utils.db_update_task(id_task)
    return msg

@app.route(f"{PATH_BASE_API}/tasks/delete/<id_task>", methods = ['DELETE'])
def delete_task(id_task):
    msg = utils.db_delete_task(id_task)
    return msg


if __name__== '__main__':
    app.run(debug=True)