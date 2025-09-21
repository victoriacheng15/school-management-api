# Architecture

## Overview

This project is a RESTful API built with Flask for managing a school database system. It supports typical operations like adding, updating, reading, and archiving entities such as students, instructors, departments, courses, and more.

The architecture follows a layered approach, separating routing, business logic, and database access.

## Technology Stack

- Flask – API framework
- PostgreSQL (Docker container) – Local development
- Azure Database for PostgreSQL – Cloud database (production)
- Azure Container Registry (ACR) – Container image storage
- Azure Web App – Frontend/client application
- Docker – Containerization
- Gunicorn – WSGI server
- GitHub Actions – CI for format, test, coverage, and markdown linting

## Component Diagram

```mermaid
flowchart TD
    ClientTool["Client (Azure Web App / curl / Postman)"]

    subgraph "API Layer"
        Routes["Flask Routes (routes/)"]
    end

    subgraph "Business Logic Layer"
        Services["Service Layer (services/)"]
    end

    subgraph "Shared Utilities"
        Utils["Utilities (utils/)"]
    end

    subgraph "Data Access Layer"
        DB["Raw SQL Access (db/)"]
        LocalPG["PostgreSQL (Docker Compose)"]
        AzurePG["Azure Database for PostgreSQL"]
    end

    ClientTool --> Routes
    Routes --> Services
    Routes --> Utils
    Services --> Utils
    Services --> DB
    DB --> LocalPG
    DB --> AzurePG
```

## Key Components

- Client: Any tool or user agent—like Postman, curl, or a web browser—used to send HTTP requests to the API.
- Flask API Routes: Defines HTTP endpoints (e.g., /students, /courses) that handle requests, parse inputs, and send responses.
- Service Layer: Contains business logic such as data validation, processing rules, and orchestration between routes and the database layer.
- Database Layer: Responsible for executing raw SQL queries or ORM operations to interact with the PostgreSQL database (local via Docker Compose, production via Azure Database for PostgreSQL).
- PostgreSQL: The persistent database that stores all application data according to your defined schema. Local development uses Docker Compose, while production uses Azure Database for PostgreSQL.

## Request Flow

```mermaid
sequenceDiagram
    participant Client
    participant Flask as "Flask Route"
    participant Service as "StudentService"
    participant DB as "DB Layer"
    participant PostgreSQL as "PostgreSQL (Local/Azure)"

    Client->>Flask: POST /students
    Flask->>Service: validate & process data
    alt Data valid
        Service->>DB: insert student
        DB->>PostgreSQL: INSERT INTO students (...)
        PostgreSQL-->>DB: OK
        DB-->>Service: success
        Service-->>Flask: return 201 Created
        Flask-->>Client: 201 Created + JSON success response
    else Data invalid / error occurs
        Service-->>Flask: return error message + status code
        Flask-->>Client: Error response (400, 500, etc.) + JSON error message
    end
```

**Note**: This request flow pattern applies to all CRUD operations with the following variations:

**HTTP Methods and Endpoints:**

- `GET /students` (read all)
- `GET /students/{id}` (read by ID)
- `POST /students` (create)
- `PUT /students` (update)
- `PATCH /students` (archive/soft delete)

**SQL Operations:**

- `INSERT INTO students (...)` (create)
- `SELECT * FROM students WHERE id = ?` (read)
- `UPDATE students SET ... WHERE id = ?` (update/patch)
- `DELETE FROM students WHERE id = ?` (delete)

**Response Status Codes:**

- `201 Created` (POST - successful creation)
- `200 OK` (GET, PUT, PATCH, DELETE - successful operations)
- `400 Bad Request` (invalid data or missing required fields)
- `404 Not Found` (when resource doesn't exist)
- `422 Unprocessable Entity` (archive operations when resource not found)
- `500 Internal Server Error` (unexpected server errors)

## Folder Structure

```plaintext
```plaintext
project/
├── run.py                      # Flask app entry point
├── app/                        # Main application package
│   ├── __init__.py             # App factory, extensions initialization
│   ├── models/                 # Data models (schemas, dataclasses)
│   ├── routes/                 # API endpoints (controllers)
│   ├── services/               # Business logic layer
│   ├── utils/                  # Reusable helpers
├── db/                         # Database layer
│   ├── data.py                 # Initial data population
│   ├── database.py             # Main DB connection logic
│   ├── db_utils.py             # Helper functions for DB
│   ├── init_postgresql.py      # DB initialization script
│   ├── schema_postgresql.sql   # DB schema
├── scripts/                    # Scripts to run and automate project tasks
├── tests/                      # Unit tests
├── docs/                       # Project documentation
├── requirements.txt            # Python dependencies
├── Dockerfile                  # Single-stage Docker build
├── Dockerfile.multi-stage      # Multi-stage Docker build
├── entrypoint.sh               # Docker container entrypoint script
├── Makefile                    # Convenience commands (build, run, test)
├── api_client.sh               # API testing helper script
├── checklist.md                # Project checklist
└── .github/
    └── workflows/
        └── ci.yml              # CI workflow for format, test, coverage
        └── markdownlint.yml    # CI workflow for format markdown files
```
