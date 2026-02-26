from fastapi.testclient import TestClient
from main import app
import main
import pytest

client = TestClient(app)

@pytest.fixture(autouse=True)
def reset_todos():
    main.Todos.clear()
    main.Todos.extend([
        {"id": 1, "title": "Buy groceries", "completed": False},
        {"id": 2, "title": "Clean the house", "completed": True},
    ])

def test_root():
    r = client.get("/")
    assert r.status_code == 200
    data = r.json()
    assert "message" in data
    assert "endpoints" in data


def test_create_todo_fields():
    r = client.post("/todos", json={"title": "pytest todo", "completed": False})
    assert r.status_code == 201
    data = r.json()
    assert data["title"] == "pytest todo"
    assert data["completed"] is False
    assert "created_at" in data
    assert "completed_at" in data


def test_get_all_todos():
    response = client.get("/todos")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_get_todo_by_id_success():
    response = client.get("/todos/1")
    assert response.status_code ==200
    data = response.json()
    assert data["id"] == 1
    assert "title" in data
    assert "completed" in data


def test_get_todo_by_id_not_found():
    response = client.get("/todos/9999")
    assert response.status_code == 404
    assert response.json()["detail"] == "Todo not found"

def test_create_todo_success():    
    response = client.post("/todos", json={
        "title": "Test new task", 
        "completed": False
    })
    assert response.status_code ==201
    data= response.json()
    assert "id" in data
    assert "title" in data
    assert "completed" in data

def test_delete_todo_success():
    response = client.delete("/todos/1")
    assert response.status_code ==204

    followup = client.get("/todos/1")
    assert followup.status_code ==404

def test_put_todo_success():    
    response = client.put("/todos/1", json={
        "title": "Updated via test",
        "completed" : True
    })
    assert response.status_code == 200
    data= response.json()
    assert data["id"] ==1
    assert data["title"] == "Updated via test"
    assert data["completed"] is True



