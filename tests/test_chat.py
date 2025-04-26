import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_process_chat():
    response = client.post("/chat", json={"user_input": "Hello, how are you?"})
    assert response.status_code == 200
    assert "bot_response" in response.json()

def test_process_chat_empty_input():
    response = client.post("/chat", json={"user_input": ""})
    assert response.status_code == 400
    assert response.json() == {"detail": "User input cannot be empty."}