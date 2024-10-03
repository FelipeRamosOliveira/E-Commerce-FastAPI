# tests/test_cart.py
import uuid
import pytest
from fastapi.testclient import TestClient
from backend.app import app  # Ajuste o caminho de importação conforme necessário

client = TestClient(app)

def test_add_to_cart():
    # Primeiro, registre um usuário para garantir que o sistema está funcionando
    unique_username = f"user_test_{uuid.uuid4()}"  # Gera um nome de usuário único
    client.post("/users/", json={
        "username": unique_username,
        "password": "securepassword"
    })
    
    # Teste a adição de um produto ao carrinho
    response = client.post("/add-to-cart/", json={"product_name": "Skol"})  # Use `json` para enviar o nome do produto
    assert response.status_code == 200  # Verifica se o status é 200
    assert "Skol added to cart" in response.json()["message"]  # Verifica a mensagem de resposta



