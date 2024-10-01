import pytest
from fastapi.testclient import TestClient
from backend.app import app

client = TestClient(app)

def test_create_product():
    product_data = {
        "name": "Ambev Beer",
        "description": "Refreshing beer from Ambev",
        "price": 10.0
    }
    response = client.post("/products/", json=product_data)
    assert response.status_code == 200
    assert response.json()["name"] == product_data["name"]

def test_create_product_duplicate():
    product_data = {
        "name": "Ambev Beer",
        "description": "Refreshing beer from Ambev",
        "price": 10.0
    }
    response = client.post("/products/", json=product_data)  # Try to create the same product again
    assert response.status_code == 400
    assert response.json()["detail"] == "Product already exists"
