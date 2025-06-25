from app.tasks.schemas import TaskCreate
from app.tasks.repository import TaskRepository
from app.auth.repository import UserRepository
from app.auth.schemas import UserCreate


def test_create_task(client, db_session):
    # Setup test user
    user_repo = UserRepository(db_session)
    user_repo.create_user(UserCreate(email="test@example.com", password="password123"))

    # Login to get token
    login_response = client.post(
        "/api/v1/users/login",
        json={"email": "test@example.com", "password": "password123"},
    )
    token = login_response.json()["access_token"]

    # Test create task
    response = client.post(
        "/api/v1/tasks/",
        json={"title": "Test task", "description": "Test description"},
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "Test task"
    assert data["description"] == "Test description"
    assert "id" in data
    assert "owner_id" in data
    assert "created_at" in data

    # Test create task without auth
    response = client.post(
        "/api/v1/tasks/", json={"title": "Test task", "description": "Test description"}
    )
    assert response.status_code == 401

    # Test invalid task data
    response = client.post(
        "/api/v1/tasks/",
        json={"title": "", "description": "Test description"},  # Empty title
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 422


def test_get_tasks(client, db_session):
    # Setup test user and tasks
    user_repo = UserRepository(db_session)
    user = user_repo.create_user(
        UserCreate(email="test1@example.com", password="password123")
    )
    task_repo = TaskRepository(db_session)
    task_repo.create_user_task(user.id, TaskCreate(title="Task 1"))
    task_repo.create_user_task(user.id, TaskCreate(title="Task 2"))

    # Login to get token
    login_response = client.post(
        "/api/v1/users/login",
        json={"email": "test1@example.com", "password": "password123"},
    )
    token = login_response.json()["access_token"]

    # Test get all tasks
    response = client.get(
        "/api/v1/tasks/", headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
    tasks = response.json()
    assert len(tasks) == 2
    assert tasks[0]["title"] == "Task 1"
    assert tasks[1]["title"] == "Task 2"

    # Test without auth
    response = client.get("/api/v1/tasks/")
    assert response.status_code == 401


def test_get_single_task(client, db_session):
    # Setup test users and tasks
    user_repo = UserRepository(db_session)
    user1 = user_repo.create_user(
        UserCreate(email="user1@example.com", password="password123")
    )
    user_repo.create_user(UserCreate(email="user2@example.com", password="password123"))
    task_repo = TaskRepository(db_session)
    task = task_repo.create_user_task(user1.id, TaskCreate(title="User1 Task"))

    # Login as user1 (owner)
    login_response = client.post(
        "/api/v1/users/login",
        json={"email": "user1@example.com", "password": "password123"},
    )
    token = login_response.json()["access_token"]

    # Test get own task
    response = client.get(
        f"/api/v1/tasks/{task.id}", headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
    assert response.json()["title"] == "User1 Task"

    # Login as user2 (not owner)
    login_response = client.post(
        "/api/v1/users/login",
        json={"email": "user2@example.com", "password": "password123"},
    )
    token = login_response.json()["access_token"]

    # Test get other user's task
    response = client.get(
        f"/api/v1/tasks/{task.id}", headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 403  # or 404 depending on your implementation


def test_update_task(client, db_session):
    # Setup test user and task
    user_repo = UserRepository(db_session)
    user = user_repo.create_user(
        UserCreate(email="test31@example.com", password="password123")
    )
    task_repo = TaskRepository(db_session)
    task = task_repo.create_user_task(user.id, TaskCreate(title="Original Title"))

    # Login to get token
    login_response = client.post(
        "/api/v1/users/login",
        json={"email": "test31@example.com", "password": "password123"},
    )
    token = login_response.json()["access_token"]

    # Test update task
    response = client.put(
        f"/api/v1/tasks/{task.id}",
        json={"title": "Updated Title", "description": "New description"},
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Updated Title"
    assert data["description"] == "New description"

    # Test update non-existent task
    response = client.put(
        "/api/v1/tasks/nonexistent-id",
        json={"title": "Updated Title"},
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 404


def test_delete_task(client, db_session):
    # Setup test user and task
    user_repo = UserRepository(db_session)
    user = user_repo.create_user(
        UserCreate(email="testaa@example.com", password="password123")
    )
    task_repo = TaskRepository(db_session)
    task = task_repo.create_user_task(user.id, TaskCreate(title="Task to delete"))

    # Login to get token
    login_response = client.post(
        "/api/v1/users/login",
        json={"email": "testaa@example.com", "password": "password123"},
    )
    token = login_response.json()["access_token"]

    # Test delete task
    response = client.delete(
        f"/api/v1/tasks/{task.id}", headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 204

    # Verify task is deleted
    response = client.get(
        f"/api/v1/tasks/{task.id}", headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 404
