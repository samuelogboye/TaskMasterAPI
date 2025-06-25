from app.auth.schemas import UserCreate
from app.auth.repository import UserRepository


def test_register_user(client, db_session):
    # Test successful registration
    response = client.post(
        "/api/v1/users/register",
        json={"email": "test11@example.com", "password": "password123"},
    )
    print("response", response.status_code, response.json())
    assert response.status_code == 201
    data = response.json()
    assert "email" in data
    assert data["email"] == "test11@example.com"
    assert "id" in data
    assert "hashed_password" not in data  # Password should never be returned

    # Test duplicate email registration
    response = client.post(
        "/api/v1/users/register",
        json={"email": "test11@example.com", "password": "password123"},
    )
    assert response.status_code == 400
    assert "Email already registered" in response.json()["detail"]["error"]

    # Test invalid email format
    response = client.post(
        "/api/v1/users/register",
        json={"email": "notanemail", "password": "password123"},
    )
    assert response.status_code == 422

    # Test short password
    response = client.post(
        "/api/v1/users/register", json={"email": "test2@example.com", "password": "123"}
    )
    assert response.status_code == 422


def test_login_user(client, db_session):
    # Setup test user
    user_repo = UserRepository(db_session)
    user_repo.create_user(
        UserCreate(email="test12@example.com", password="password123")
    )

    # Test successful login
    response = client.post(
        "/api/v1/users/login",
        json={"email": "test12@example.com", "password": "password123"},
    )
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"

    # Test wrong password
    response = client.post(
        "/api/v1/users/login",
        json={"email": "test12@example.com", "password": "wrongpassword"},
    )
    assert response.status_code == 401

    # Test non-existent user
    response = client.post(
        "/api/v1/users/login",
        json={"email": "nonexistent@example.com", "password": "password123"},
    )
    assert response.status_code == 401


def test_get_current_user(client, db_session):
    # Setup test user
    user_repo = UserRepository(db_session)
    user_repo.create_user(
        UserCreate(email="test01@example.com", password="password123")
    )

    # Login to get token
    login_response = client.post(
        "/api/v1/users/login",
        json={"email": "test01@example.com", "password": "password123"},
    )
    token = login_response.json()["access_token"]

    # Test get current user
    response = client.get(
        "/api/v1/users/me", headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == "test01@example.com"

    # Test without token
    response = client.get("/api/v1/users/me")
    assert response.status_code == 401

    # Test with invalid token
    response = client.get(
        "/api/v1/users/me", headers={"Authorization": "Bearer invalidtoken"}
    )
    assert response.status_code == 401
