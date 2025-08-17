from fastapi.testclient import TestClient
from app.main import app, professionals, appointments

client = TestClient(app)

def test_list_professionals():
    response = client.get("/professionals")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == len(professionals)
    assert data[0]["name"] == professionals[0].name

def test_create_appointment():
    appointments.clear()
    payload = {"client_name": "山田太郎", "scheduled_time": "2025-01-01T10:00:00"}
    response = client.post("/professionals/1/appointments", json=payload)
    assert response.status_code == 201
    assert len(appointments) == 1
    assert appointments[0].client_name == "山田太郎"

def test_list_columns():
    response = client.get("/columns")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_list_communities_and_post_message():
    response = client.get("/communities")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
    message = {"message": "こんにちは"}
    response_post = client.post("/communities/1/messages", json=message)
    assert response_post.status_code == 201


def test_index_served():
    response = client.get("/")
    assert response.status_code == 200
    assert "text/html" in response.headers["content-type"]
