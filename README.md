# E-Commerce API

This is a simple e-commerce API built with FastAPI. It allows users to register, add products to a shopping cart, and view their cart's contents.

## Directory Structure

```
.
├── backend
│   ├── __init__.py
│   ├── app.py
│   ├── auth.py
│   ├── database.py
│   ├── logging.py
│   ├── models.py
│   ├── operations.py
│   └── schemas.py
├── database
│   └── ecommerce.db
├── poetry.lock
├── pyproject.toml
├── pytest.ini
├── run.py
├── test.db
└── tests
    ├── __init__.py
    └── test_cart.py
```

## Installation

To set up this project, follow these steps:

1. **Install Poetry** (if you haven't already):

   Follow the instructions at [Poetry's official website](https://python-poetry.org/docs/#installation) to install Poetry.

2. **Clone the repository**:

   ```bash
   git clone <your-repo-url>
   cd <your-repo-directory>
   ```

3. **Install the dependencies**:

   ```bash
   poetry install
   ```

## Running the Application

To run the FastAPI application, use the following command:

```bash
poetry run python run.py
```

Once the server is running, you can access the API documentation at `http://127.0.0.1:8000/docs`.

## API Endpoints

### User Registration

- **POST /users/**: Register a new user.
  - **Request Body**:
    ```json
    {
      "username": "your_username",
      "password": "your_password"
    }
    ```

### Add to Cart

- **POST /add-to-cart/**: Add a product to the cart.
  - **Request Body**:
    ```json
    {
      "product_name": "Skol"
    }
    ```

### View Cart

- **GET /cart/**: View the current contents of the cart.

## Testing

To run the tests, use the following command:

```bash
poetry run pytest
```

This will execute the tests defined in the `tests` directory.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
