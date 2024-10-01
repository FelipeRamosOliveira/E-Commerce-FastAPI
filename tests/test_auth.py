import sys
import os

# Add the project root to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pytest
from fastapi.testclient import TestClient
from backend.app import app
from backend.database import SessionLocal
from backend.schemas import UserCreate

client = TestClient(app)

@pytest.fixture(scope="module")
def db():
    # Create a new database session for the tests
    db = SessionLocal()
    yield db
    db.close()

def test_create_user(db):
    user_data = {"username": "testuser", "password": "testpassword"}
    response = client.post("/users/", json=user_data)
    assert response.status_code == 200
    assert response.json()["username"] == user_data["username"]

# def test_create_user_duplicate(db):
#     user_data = {"username": "testuser", "password": "testpassword"}
#     response = client.post("/users/", json=user_data)  # Try to create the same user again
#     assert response.status_code == 400
#     assert response.json()["detail"] == "Username already registered"

# def test_get_products():
#     response = client.get("/products/")
#     assert response.status_code == 200
#     assert isinstance(response.json(), list)  # Ensure it returns a list

