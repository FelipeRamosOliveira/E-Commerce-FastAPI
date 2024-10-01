import pytest
from fastapi.testclient import TestClient
from backend.app import app

client = TestClient(app)

def test_create_order():
    order_data = {
        "user_id": 1,  # Replace with a valid user ID
        "products": ["1", "2"]  # Replace with valid product IDs
    }
    response = client.post("/orders/", json=order_data)
    assert response.status_code == 200
    assert response.json()["user_id"] == order_data["user_id"]
