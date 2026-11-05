# Task Management API

A production-ready, highly professional asynchronous Task Management REST API built with FastAPI, PostgreSQL, and SQLAlchemy 2.0.

## Features

- **User Authentication**: JWT-based authentication with access and refresh tokens
- **Task Management**: Full CRUD operations for tasks with user ownership
- **Asynchronous Design**: Built with async/await patterns for optimal performance
- **Database Migrations**: Alembic integration for database version control
- **API Documentation**: Interactive Swagger UI at `/docs`
- **Containerization**: Docker and Docker Compose for easy deployment
- **Type Safety**: Full type hints with Pydantic v2 validation
- **Security**: Password hashing with bcrypt, secure token generation

## Tech Stack

- **Framework**: FastAPI 0.115.0
- **Database**: PostgreSQL 16
- **ORM**: SQLAlchemy 2.0 (async engine)
- **Validation**: Pydantic v2 + Pydantic-Settings
- **Authentication**: JWT (python-jose) + bcrypt
- **Migrations**: Alembic
- **Containerization**: Docker & Docker Compose
- **ASGI Server**: Uvicorn

## Project Architecture

```
.
├── src/
│   ├── api/
│   │   └── v1/
│   │       ├── auth.py          # Authentication endpoints
│   │       ├── tasks.py         # Task CRUD endpoints
│   │       └── api.py           # API router aggregation
│   ├── core/
│   │   ├── config.py            # Application settings (Pydantic-Settings)
│   │   ├── database.py          # Database connection and session management
│   │   ├── security.py          # JWT and password hashing utilities
│   │   └── deps.py              # FastAPI dependencies (authentication)
│   ├── models/
│   │   ├── user.py              # User model
│   │   └── task.py              # Task model
│   ├── schemas/
│   │   ├── user.py              # User Pydantic schemas
│   │   └── task.py              # Task Pydantic schemas
│   ├── services/
│   │   ├── auth_service.py      # Authentication business logic
│   │   └── task_service.py      # Task business logic
│   └── main.py                  # FastAPI application entry point
├── alembic/
│   ├── versions/                # Database migration files
│   ├── env.py                   # Alembic environment configuration
│   └── script.py.mako           # Migration template
├── docker-compose.yml           # Docker Compose configuration
├── Dockerfile                   # Docker image configuration
├── requirements.txt             # Python dependencies
├── .env.example                 # Environment variables template
└── README.md                    # This file
```

## Quickstart Guide

### Prerequisites

- Docker and Docker Compose installed
- Git (optional, for cloning)

### Installation

1. **Clone or download the project**

```bash
cd "FastApi Service"
```

2. **Configure environment variables**

Copy the example environment file:

```bash
cp .env.example .env
```

Edit `.env` to customize settings (optional for development):

```env
DATABASE_URL=postgresql+asyncpg://postgres:postgres@db:5432/taskmanager
SECRET_KEY=your-secret-key-here-change-in-production
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
REFRESH_TOKEN_EXPIRE_DAYS=7
```

3. **Start the application with Docker Compose**

```bash
docker compose up --build
```

This will:
- Build the FastAPI application Docker image
- Start PostgreSQL database
- Run database migrations
- Start the FastAPI server on `http://localhost:8000`

4. **Access the API**

- **API Documentation (Swagger UI)**: http://localhost:8000/docs
- **ReDoc Documentation**: http://localhost:8000/redoc
- **Health Check**: http://localhost:8000/health

### Running Migrations Manually

If you need to run migrations manually:

```bash
docker compose exec web alembic upgrade head
```

### Stopping the Application

```bash
docker compose down
```

To remove volumes (deletes database data):

```bash
docker compose down -v
```

## API Endpoints

### Authentication

#### Register User
- **POST** `/api/v1/auth/register`
- **Description**: Register a new user account
- **Request Body**:
```json
{
  "email": "user@example.com",
  "username": "johndoe",
  "password": "securepassword123"
}
```
- **Response**: User object with ID, email, username, and timestamps

#### Login
- **POST** `/api/v1/auth/login`
- **Description**: Authenticate user and receive tokens
- **Request Body**:
```json
{
  "email": "user@example.com",
  "password": "securepassword123"
}
```
- **Response**: Access token and refresh token

#### Get Current User
- **GET** `/api/v1/auth/me`
- **Description**: Get the current authenticated user's profile
- **Headers**: `Authorization: Bearer <access_token>`
- **Response**: User object

### Tasks

#### Create Task
- **POST** `/api/v1/tasks`
- **Description**: Create a new task for the authenticated user
- **Headers**: `Authorization: Bearer <access_token>`
- **Request Body**:
```json
{
  "title": "Complete project documentation",
  "description": "Write comprehensive README and API docs",
  "completed": false
}
```
- **Response**: Created task object

#### Get All Tasks
- **GET** `/api/v1/tasks`
- **Description**: Get all tasks for the authenticated user with pagination
- **Headers**: `Authorization: Bearer <access_token>`
- **Query Parameters**:
  - `skip` (optional): Number of tasks to skip (default: 0)
  - `limit` (optional): Number of tasks per page (default: 10, max: 100)
- **Response**: Paginated list of tasks with metadata

#### Get Task by ID
- **GET** `/api/v1/tasks/{task_id}`
- **Description**: Get a specific task by ID
- **Headers**: `Authorization: Bearer <access_token>`
- **Response**: Task object

#### Update Task
- **PUT** `/api/v1/tasks/{task_id}`
- **Description**: Update a specific task
- **Headers**: `Authorization: Bearer <access_token>`
- **Request Body** (all fields optional):
```json
{
  "title": "Updated task title",
  "description": "Updated description",
  "completed": true
}
```
- **Response**: Updated task object

#### Delete Task
- **DELETE** `/api/v1/tasks/{task_id}`
- **Description**: Delete a specific task
- **Headers**: `Authorization: Bearer <access_token>`
- **Response**: 204 No Content

## Example Usage

### 1. Register a new user

```bash
curl -X POST "http://localhost:8000/api/v1/auth/register" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "username": "testuser",
    "password": "TestPassword123"
  }'
```

### 2. Login to get tokens

```bash
curl -X POST "http://localhost:8000/api/v1/auth/login" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "password": "TestPassword123"
  }'
```

Save the `access_token` from the response.

### 3. Create a task

```bash
curl -X POST "http://localhost:8000/api/v1/tasks" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Learn FastAPI",
    "description": "Build a REST API with FastAPI"
  }'
```

### 4. Get all tasks

```bash
curl -X GET "http://localhost:8000/api/v1/tasks" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

### 5. Update a task

```bash
curl -X PUT "http://localhost:8000/api/v1/tasks/1" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "completed": true
  }'
```

### 6. Delete a task

```bash
curl -X DELETE "http://localhost:8000/api/v1/tasks/1" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

## Database Schema

### Users Table
- `id`: Integer (Primary Key)
- `email`: String (Unique, Indexed)
- `username`: String (Unique, Indexed)
- `hashed_password`: String
- `created_at`: DateTime
- `updated_at`: DateTime

### Tasks Table
- `id`: Integer (Primary Key)
- `title`: String
- `description`: Text (Nullable)
- `completed`: Boolean (Default: False)
- `user_id`: Integer (Foreign Key → users.id)
- `created_at`: DateTime
- `updated_at`: DateTime

**Relationship**: User has many Tasks (1-to-Many)

## Security Features

- **Password Hashing**: Uses bcrypt with salt for secure password storage
- **JWT Tokens**: Access tokens (30 min expiry) and refresh tokens (7 days expiry)
- **Token Validation**: Automatic token validation on protected endpoints
- **User Isolation**: Tasks are scoped to the authenticated user
- **CORS**: Configured for cross-origin requests (configure for production)

## Development

### Running without Docker (Development)

1. **Install dependencies**

```bash
pip install -r requirements.txt
```

2. **Set up PostgreSQL**

Ensure PostgreSQL is running and create a database:

```sql
CREATE DATABASE taskmanager;
```

3. **Configure environment**

Copy `.env.example` to `.env` and update `DATABASE_URL`:

```env
DATABASE_URL=postgresql+asyncpg://postgres:yourpassword@localhost:5432/taskmanager
```

4. **Run migrations**

```bash
alembic upgrade head
```

5. **Start the server**

```bash
uvicorn src.main:app --reload --host 0.0.0.0 --port 8000
```

### Code Quality

- **PEP 8**: Follows Python style guidelines
- **Type Hints**: Full type annotations throughout
- **Async/Await**: Proper async patterns for database operations
- **Error Handling**: Comprehensive HTTP status codes and error messages

## Production Considerations

- Change `SECRET_KEY` in environment variables
- Set `DEBUG=False` in production
- Configure CORS origins appropriately
- Use environment-specific `DATABASE_URL`
- Implement rate limiting
- Add logging and monitoring
- Use HTTPS in production
- Consider adding refresh token rotation
- Implement password strength requirements

## License

This project is for educational and portfolio purposes.

## Author

Built as a developer portfolio project demonstrating production-ready FastAPI application development.
