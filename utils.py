import sqlite3
from flask import jsonify, request
from werkzeug.security import generate_password_hash, check_password_hash

conn = sqlite3.connect("taskapp.db", check_same_thread=False)
c = conn.cursor()

def create_tables():
    query = """
            CREATE TABLE task (
                id_task INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT,
                description TEXT,
                isCompletet INTEGER,
                userAsigned INTEGER
            );
    """
    try:
        c.execute(query,)
        msg = "Tablas creadas"
    except Exception as err:
        msg = "Tablas ya existentes"
        print(err)
    return msg

#Aquí comienzan las funciones para trabajar en la tabla users

def db_create_user(first_name, last_name, email, password, confirm_password):
    pass_cifr = generate_password_hash(password)
    same = check_password_hash(pass_cifr, confirm_password)
    if same:
        query =("INSERT INTO users (first_name, last_name, email, password) VALUES (?,?,?,?)")
        parameters = (first_name, last_name, email, pass_cifr)
        c.execute(query, parameters)
        conn.commit()
        msg = "Nuevo usuario creado"
    else:
        msg = "Las contraseñas no coiciden"
    return msg

def db_get_user(id_user):
    query = f"SELECT id_user, first_name, last_name, email FROM users WHERE id_user == {id_user}"
    try:
        c.execute(query,)
        conn.commit()
        datos = c.fetchone()
        if datos != None:
            usuario = {"id_user":datos[0], "First_name":datos[1], "Last_name":datos[2], "Email":datos[3]}
            msg = jsonify({"Usuario":usuario, "Mensaje": "Usuario encontrado"})
            return msg
        msg = "Usuario encontrado"
    except Exception:
        msg = "Hubo un error al buscar usuario"
    return msg

def db_delete_user(id_user):
    query = f"DELETE FROM users WHERE id_user == {id_user}"
    try:
        c.execute(query,)
        conn.commit()
        msg = "Usuario eliminado"
    except Exception:
        msg = "Hubo un error al eliminar usuario"
    return msg

def db_update_user(id_user):
    query = """UPDATE users SET first_name = '{0}', last_name = '{1}', email = '{2}'
               WHERE id_user = '{3}'
               """.format(request.json['first_name'],request.json['last_name'],request.json['email'], id_user)
    try:
        c.execute(query,)
        conn.commit()
        msg = "Usuario actualizado"
    except Exception:
        msg = "Hubo un error al actualizar usuario"
    return msg

#Aquí comienzan las funciones para trabajar en la tabla tasks

def db_create_task(title, description, is_completed, user_asigned):
    """
    Crea nueva tarea, recibe:
    title
    description
    is_completed (0->Incompleta  1->Completa)
    user_asigned
    """
    query = ("INSERT INTO tasks (title, description, isCompleted, userAsigned) VALUES (?,?,?,?)")
    parameters = (title, description, is_completed, user_asigned)
    try:
        c.execute(query, parameters)
        conn.commit()
        msg = "Tarea creada"
    except Exception as err:
        msg = "Error al crear tarea"
        print(err)
    return msg

def db_get_task(id_user):
    query = (f"SELECT id_task, title, description, isCompleted FROM tasks WHERE userAsigned == {id_user}")
    try:
        c.execute(query,)
        conn.commit()
        datos = c.fetchall()
        tareas=[]
        for dato in datos:
            tarea = {'id_task':dato[0],'Title':dato[1],'Description':dato[2], 'isCompleted':dato[3]}
            tareas.append(tarea)
        return tareas
    except Exception as err:
        msg = {'Msg':'Error al buscar tarea'}
        print(err)
    return msg

def db_update_task(id_task):
    query = """UPDATE tasks SET title = '{0}', description = '{1}', isCompleted = '{2}', userAsigned = '{3}'
               WHERE id_task = '{4}'
               """.format(request.json['title'],request.json['description'],request.json['isCompleted'],request.json['userAsigned'], id_task)
    try:
        c.execute(query,)
        conn.commit()
        msg = "Tarea actualizada"
    except Exception:
        msg = "Hubo un error al actualizar tarea"
    return msg

def db_delete_task(id_task):
    query = f"DELETE FROM tasks WHERE id_task == {id_task}"
    try:
        c.execute(query,)
        conn.commit()
        msg = "Tarea Eliminada"
    except Exception as err:
        msg = "Hubo un error al eliminar la tarea"
        print(err)
    return msg