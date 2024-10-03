# tests/test_cart.py
import uuid
import pytest
from fastapi.testclient import TestClient
from backend.app import app  # Ajuste o caminho de importação conforme necessário

# tests/test_auth.py

client = TestClient(app)

def test_successful_registration():
    unique_username = f"user_{uuid.uuid4()}"  # Gera um nome de usuário único
    response = client.post("/users/", json={
        "username": unique_username,
        "password": "securepassword"
    })
    print(response.json())  # Para verificar o conteúdo da resposta
    assert response.status_code in {200, 201}  # Aceitar ambos os status


def test_add_to_cart():
    response = client.post("/add-to-cart/", json={"product_name": "Skol", "quantity": 2})
    assert response.status_code == 200
    assert "Skol added to cart" in response.json()["message"]

def test_view_cart():
    response = client.get("/cart/")
    assert response.status_code == 200
    assert "cart" in response.json()


