# Backend API - Personal Finance Tracker

This FastAPI project provides RESTful and websocket APIs for authentication, transaction and budget management, receipt OCR, and push notifications.

## Features

- User registration & authentication (JWT-based)
- CRUD for transactions (with category/tag filtering)
- Budget and progress with threshold alerts
- Placeholder endpoints for receipt OCR
- WebSocket-based notification infrastructure
- PostgreSQL integration

## Local Setup

1. **Python Version:** Python 3.10+
2. **Install dependencies:**
    ```shell
    python -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt
    ```
3. **Configure environment variables:**  
   Copy `.env.example` to `.env` and fill in credentials for database and secrets.

4. **Apply migrations and run server:**
    ```shell
    alembic upgrade head
    uvicorn main:app --reload
    ```

5. **Run tests:**
    ```shell
    pytest
    ```

## Directory Structure

- `main.py` - FastAPI app factory
- `models/` - SQLAlchemy data models
- `schemas/` - Pydantic models
- `crud/` - CRUD functions
- `api/` - API routers
- `core/` - Config, auth, dependencies
- `tests/` - Pytest test cases
- `alembic/` - DB migrations

## Docker

Build and run with Docker:
```shell
docker build -t backend_api .
docker run --env-file .env -p 8000:8000 backend_api
```

---
- OpenAPI docs: `http://localhost:8000/docs`
- WebSocket notifications: See `/ws/notifications` in API docs

