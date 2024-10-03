import uuid
from fastapi.testclient import TestClient
from backend.app import app  

# Create a TestClient instance to simulate API requests
client = TestClient(app)

def test_sucess_home():
    """
    Test the root endpoint ('/') to ensure that the server is running properly.
    Should return a 200 OK status.
    """
    response = client.get("/")
    assert response.status_code == 200

def test_sucess_add_user():
    """
    Test the user registration endpoint ('/users/').

    - Generates a unique username using UUID to avoid conflicts.
    - Posts the new user data and checks if the status code is 200 or 201.
    - Verifies the response contains the correct user data and includes a user ID.
    """
    # Generate a unique username to avoid conflicts
    unique_username = f"user_{uuid.uuid4()}"
    
    # Send the POST request to register a new user
    response = client.post("/users/", json={
        "username": unique_username,
        "password": "securepassword"
    })
    
    # Assert that the response status code is 200 or 201 (user created successfully)
    assert response.status_code in [200, 201]
    
    # Check if the username and ID are returned correctly in the response
    data = response.json()
    assert data["username"] == unique_username  # Ensure the username matches
    assert "id" in data  # Verify the user ID is returned

def test_fail_add_to_cart():
    """
    Test the failure scenario for adding a product to the cart ('/add-to-cart/').

    - Sends an invalid request (invalid token in headers).
    - Ensures the response returns a 422 Unprocessable Entity status.
    """
    response = client.post("/add-to-cart/", headers={"X-Token": "coneofsilence"}, json={"product_name": "Skol"}) 
    assert response.status_code == 422

def test_sucess_view_cart():
    """
    Test the view cart endpoint ('/cart/').

    - Sends a GET request to view the cart.
    - Verifies the response status is 200 and that the 'cart' key is in the returned JSON.
    """
    response = client.get("/cart/")
    assert response.status_code == 200 
    assert "cart" in response.json()
