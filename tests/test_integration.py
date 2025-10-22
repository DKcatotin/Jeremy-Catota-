"""Tests de integración para la API"""
import pytest
import sys
import os

# Agregar el directorio raíz al path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import app


@pytest.fixture
def client():
    """Cliente de prueba para Flask"""
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


class TestAPIEndpoints:
    """Tests de endpoints de la API"""
    
    def test_home_endpoint(self, client):
        """Test del endpoint principal"""
        response = client.get('/')
        assert response.status_code == 200
        data = response.get_json()
        assert "message" in data
        assert "endpoints" in data
    
    def test_get_all_tasks(self, client):
        """Test para obtener todas las tareas"""
        response = client.get('/tasks')
        assert response.status_code == 200
        data = response.get_json()
        assert isinstance(data, list)
    
    def test_create_task(self, client):
        """Test para crear una nueva tarea"""
        new_task = {"title": "Nueva tarea de prueba"}
        response = client.post('/tasks', json=new_task)
        assert response.status_code == 201
        data = response.get_json()
        assert data["title"] == "Nueva tarea de prueba"
        assert "id" in data
        assert data["completed"] is False
    
    def test_create_task_sin_titulo(self, client):
        """Test para validar que no se puede crear tarea sin título"""
        response = client.post('/tasks', json={})
        assert response.status_code == 400
        data = response.get_json()
        assert "error" in data
    
    def test_get_task_by_id(self, client):
        """Test para obtener una tarea por ID"""
        # Primero crear una tarea
        new_task = {"title": "Tarea para buscar"}
        create_response = client.post('/tasks', json=new_task)
        task_id = create_response.get_json()["id"]
        
        # Ahora buscarla
        response = client.get(f'/tasks/{task_id}')
        assert response.status_code == 200
        data = response.get_json()
        assert data["id"] == task_id
        assert data["title"] == "Tarea para buscar"
    
    def test_get_task_not_found(self, client):
        """Test para buscar una tarea que no existe"""
        response = client.get('/tasks/9999')
        assert response.status_code == 404
    
    def test_update_task(self, client):
        """Test para actualizar una tarea"""
        # Crear tarea
        new_task = {"title": "Tarea para actualizar"}
        create_response = client.post('/tasks', json=new_task)
        task_id = create_response.get_json()["id"]
        
        # Actualizar tarea
        update_data = {"title": "Tarea actualizada", "completed": True}
        response = client.put(f'/tasks/{task_id}', json=update_data)
        assert response.status_code == 200
        data = response.get_json()
        assert data["title"] == "Tarea actualizada"
        assert data["completed"] is True
    
    def test_delete_task(self, client):
        """Test para eliminar una tarea"""
        # Crear tarea
        new_task = {"title": "Tarea para eliminar"}
        create_response = client.post('/tasks', json=new_task)
        task_id = create_response.get_json()["id"]
        
        # Eliminar tarea
        response = client.delete(f'/tasks/{task_id}')
        assert response.status_code == 204
        
        # Verificar que ya no existe
        get_response = client.get(f'/tasks/{task_id}')
        assert get_response.status_code == 404