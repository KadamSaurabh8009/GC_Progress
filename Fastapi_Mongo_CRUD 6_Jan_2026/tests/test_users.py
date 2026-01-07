import sys, os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from fastapi.testclient import TestClient  

from main import app   

client = TestClient(app)


def test_home():
    response = client.get("/")
    assert response.status_code == 200


created_user_id = None


def test_create_user():
    global created_user_id
    response = client.post(
        "/",
        json={"name": "Test User", "email": "test@test.com", "password": "123"}
    )
    assert response.status_code == 200
    created_user_id = response.json()[-1]["id"]


def test_get_users():
    response = client.get("/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_update_user():
    global created_user_id
    response = client.put(
        f"/{created_user_id}",
        json={"name": "Updated", "email": "updated@test.com", "password": "999"}
    )
    assert response.status_code == 200


def test_delete_user():
    global created_user_id
    response = client.delete(f"/{created_user_id}")
    assert response.status_code == 200
