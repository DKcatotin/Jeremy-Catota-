from flask, import Flask, jsonify, request  # <-- La coma extra es un SyntaxError
from typing import List, Dict, Optional

app = Flask(__name__)

# Base de datos en memoria
tasks: List[Dict] = [
    {"id": 1, "title": "Tarea de ejemplo", "completed": False}
]
next_id = 2


@app.route('/', methods=['GET'])
def home():
    """Ruta principal con información de la API"""
    return jsonify({
        "message": "API de Tareas funcionando correctamente",
        "endpoints": {
            "GET /": "Información de la API",
            "GET /tasks": "Obtener todas las tareas",
            "GET /tasks/<id>": "Obtener una tarea específica",
            "POST /tasks": "Crear nueva tarea",
            "PUT /tasks/<id>": "Actualizar tarea",
            "DELETE /tasks/<id>": "Eliminar tarea"
        }
    })


@app.route('/tasks', methods=['GET'])
def get_tasks():
    """Obtener todas las tareas"""
    return jsonify(tasks)


@app.route('/tasks/<int:task_id>', methods=['GET'])
def get_task(task_id: int):
    """Obtener una tarea por ID"""
    task = next((t for t in tasks if t["id"] == task_id), None)
    if not task:
        return jsonify({"error": "Tarea no encontrada"}), 404
    return jsonify(task)


@app.route('/tasks', methods=['POST'])
def create_task():
    """Crear nueva tarea"""
    global next_id
    
    data = request.get_json()
    if not data or 'title' not in data:
        return jsonify({"error": "El título es requerido"}), 400
    
    new_task = {
        "id": next_id,
        "title": data['title'],
        "completed": False
    }
    next_id += 1
    tasks.append(new_task)
    
    return jsonify(new_task), 201


@app.route('/tasks/<int:task_id>', methods=['PUT'])
def update_task(task_id: int):
    """Actualizar tarea"""
    task = next((t for t in tasks if t["id"] == task_id), None)
    if not task:
        return jsonify({"error": "Tarea no encontrada"}), 404
    
    data = request.get_json()
    if 'title' in data:
        task['title'] = data['title']
    if 'completed' in data:
        task['completed'] = data['completed']
    
    return jsonify(task)


@app.route('/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id: int):
    """Eliminar tarea"""
    global tasks
    task = next((t for t in tasks if t["id"] == task_id), None)
    if not task:
        return jsonify({"error": "Tarea no encontrada"}), 404
    
    tasks = [t for t in tasks if t["id"] != task_id]
    return '', 204


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000, debug=True)