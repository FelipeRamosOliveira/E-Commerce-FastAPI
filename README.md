# E-Commerce API

This is a simple e-commerce API built with FastAPI. It allows users to register, add products to a shopping cart, and view their cart's contents.

## Directory Structure

```sh
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
└── tests
    ├── __init__.py
    └── test_cart.py
```

## Installation

### Prerequisites

- Python 3.10 or later
- Poetry (for dependency management)

To set up this project, follow these steps:

1. **Install Poetry** (if you haven't already):

    ```bash
   pip install poetry
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
or just

```bash
python run.py
```


Once the server is running, you can access the API documentation at `http://localhost:8000/docs`.

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

## Docker Deployment

To run the application using Docker, follow these steps:

1. **Build the Docker Image**:

    ```bash
    docker build -t e-commerce-api .
    ```

2. **Run the Docker Container**:

    ```bash
    docker run -d -p 8000:8000 e-commerce-api
    ```

3. **Access the API**: 

    Once the container is running, you can access your API at `http://localhost:8000`.
