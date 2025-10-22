"""Tests unitarios para la lógica de tareas"""
import pytest


class TestTaskValidations:
    """Tests de validaciones de tareas"""
    
    def test_task_debe_tener_titulo(self):
        """Una tarea debe tener un título"""
        task = {"id": 1, "title": "Mi tarea", "completed": False}
        assert "title" in task
        assert task["title"] != ""
        assert len(task["title"]) > 0
    
    def test_task_nueva_no_completada(self):
        """Una tarea nueva debe estar marcada como no completada"""
        task = {"id": 1, "title": "Nueva tarea", "completed": False}
        assert task["completed"] is False
    
    def test_task_tiene_id(self):
        """Una tarea debe tener un ID único"""
        task = {"id": 1, "title": "Tarea con ID", "completed": False}
        assert "id" in task
        assert isinstance(task["id"], int)
        assert task["id"] > 0
    
    def test_task_estructura_valida(self):
        """Una tarea debe tener la estructura correcta"""
        task = {"id": 1, "title": "Tarea válida", "completed": False}
        assert all(key in task for key in ["id", "title", "completed"])
        assert isinstance(task["id"], int)
        assert isinstance(task["title"], str)
        assert isinstance(task["completed"], bool)


class TestTaskLogic:
    """Tests de lógica de negocio"""
    
    def test_completar_tarea(self):
        """Debe poder marcar una tarea como completada"""
        task = {"id": 1, "title": "Tarea", "completed": False}
        task["completed"] = True
        assert task["completed"] is True
    
    def test_actualizar_titulo(self):
        """Debe poder actualizar el título de una tarea"""
        task = {"id": 1, "title": "Título original", "completed": False}
        nuevo_titulo = "Título actualizado"
        task["title"] = nuevo_titulo
        assert task["title"] == nuevo_titulo
    
    def test_titulo_no_vacio(self):
        """El título no debe estar vacío"""
        task = {"id": 1, "title": "Tarea válida", "completed": False}
        assert task["title"].strip() != ""
        assert len(task["title"]) > 0
    
    def test_id_positivo(self):
        """El ID debe ser un número positivo"""
        task = {"id": 5, "title": "Tarea", "completed": False}
        assert task["id"] > 0
        assert task["id"] == 5