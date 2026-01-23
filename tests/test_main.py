from fastapi.testclient import TestClient
from app.main import app

test_client = TestClient(app)

def test_root():
    response = test_client.get("/")
    assert response.status_code == 200

def test_root_content():
    response = test_client.get("/")
    assert "html" in response.headers["content-type"]
    assert "<!DOCTYPE html>" in response.text
