
# TaskMaster API

<p align="center">
  <img src="taskmasterlogo.png" alt="TaskMaster Logo" width="200"/>
</p>
<p align="center"><em>A secure task management API with user authentication</em></p>

## Table of Contents
- [Features](#features)
- [Setup Instructions](#setup-instructions)
- [API Endpoints](#api-endpoints)
- [Authentication](#authentication)
- [Design Choices](#design-choices)
- [Testing](#testing)
- [Documentation](#documentation)

## Features

- ✅ JWT Authentication
- ✅ CRUD Operations for Tasks
- ✅ User-specific Task Isolation
- ✅ Input Validation & Sanitization
- ✅ Automatic API Documentation
- ✅ SQLite Database
- ✅ Unit Test Coverage

## Setup Instructions

### Prerequisites
- Python 3.7+
- pip package manager

### Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/samuelogboye/TaskMasterAPI.git
   cd TaskMasterAPI
   ```
2.  Create and activate virtual environment:
    
	```bash
    python -m venv venv
    # On Windows:
    venv\Scripts\activate
    # On macOS/Linux:
    source venv/bin/activate
    ```
    
3.  Install dependencies:
    
    ```bash
    pip install -r requirements.txt
    ```
    
4.  Initialize database:
    
    ```bash
    alembic upgrade head
    ```
    
5.  Run the application:
    
    ```bash
    uvicorn app.main:app --reload
    ```
    

The API will be available at  `http://localhost:8000`

## API Endpoints

### Authentication

#### Register a User

```bash
curl -X POST "http://localhost:8000/api/v1/users/register" \
  -H "Content-Type: application/json" \
  -d '{"email": "user@example.com", "password": "securepassword"}'
  ```

#### Login

```bash
curl -X POST "http://localhost:8000/api/v1/users/login" \
  -H "Content-Type: application/json" \
  -d '{"email": "user@example.com", "password": "securepassword"}'
  ```

### Tasks

#### Create Task (Authenticated)

```bash
curl -X POST "http://localhost:8000/api/v1/tasks/" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"title": "Finish project", "description": "Complete the API documentation"}'
  ```

#### Get All Tasks (Authenticated)

```bash
curl "http://localhost:8000/api/v1/tasks/" \
  -H "Authorization: Bearer YOUR_TOKEN"
  ```

#### Get Specific Task (Authenticated)

```bash
curl "http://localhost:8000/api/v1/tasks/1a2b3c4d-1234-5678-9012-abcdef123456" \
  -H "Authorization: Bearer YOUR_TOKEN"
  ```

#### Update Task (Authenticated)

```bash
curl -X PUT "http://localhost:8000/api/v1/tasks/1a2b3c4d-1234-5678-9012-abcdef123456" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"title": "Updated title", "description": "New description"}'
  ```

#### Delete Task (Authenticated)

```bash
curl -X DELETE "http://localhost:8000/api/v1/tasks/1a2b3c4d-1234-5678-9012-abcdef123456" \
  -H "Authorization: Bearer YOUR_TOKEN"
  ```

## Authentication

The API uses JWT (JSON Web Tokens) for authentication. To access protected endpoints:

1.  Register a user or use existing credentials
    
2.  Login to receive an access token
    
3.  Include the token in requests:
    
    ```text
	   Authorization: Bearer YOUR_TOKEN
    ```
Tokens expire after duration specified in the env file

## Design Choices

### Security

-   **Password Hashing**: Uses bcrypt for secure password storage
    
-   **JWT Tokens**: Stateless authentication with expiration
    
-   **Input Sanitization**: All string inputs are HTML-escaped to prevent XSS
    
-   **CORS**: Configured for development (restrict in production)
    

### Error Handling

-   **HTTP Status Codes**: Appropriate codes for each scenario
    
-   **Detailed Messages**: Clear error messages in JSON format
    
-   **Validation Errors**: Returns 422 with specific field errors
    

### Database

-   **SQLite**: Chosen for simplicity in development
    
-   **Repository Pattern**: Isolates database operations for easy testing
    
-   **Alembic Migrations**: For schema version control
    

### API Design

-   **RESTful Principles**: Proper use of HTTP methods and status codes
    
-   **Pydantic Models**: For request/response validation
    
-   **Dependency Injection**: For database sessions and auth
    

## Testing

Run the test suite with:

```bash
pytest
```

Test coverage includes:

-   Authentication flows
    
-   Task CRUD operations
    
-   Error scenarios
    
-   Validation rules
    
-   Security constraints
    

## Documentation

Interactive documentation is automatically available at:

-   Swagger UI:  `http://localhost:8000/docs`
    
-   ReDoc:  `http://localhost:8000/redoc`
    

Features:

-   Try endpoints directly
    
-   View request/response schemas
    
-   Test authentication
    
-   Automatic updates when API changes
    

## Example Workflow

1.  Register a user
    
2.  Login to get token
    
3.  Create tasks
    
4.  View your tasks
    
5.  Update/delete tasks as needed
    

All operations are scoped to the authenticated user - you'll only see and manage your own tasks.