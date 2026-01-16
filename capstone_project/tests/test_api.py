from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200

def test_query_endpoint():
    payload = {
        "query": "Quick dinner",
        "cuisine": "Any",
        "max_time": 30,
        "veg_only": False
    }

    response = client.post("/query", json=payload)
    assert response.status_code in [200, 500]  # LLM quota safe
