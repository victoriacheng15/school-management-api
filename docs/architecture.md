# Architecture

## Overview

This project is a RESTful API built with Flask for managing a school database system. It supports typical operations like adding, updating, reading, and archiving entities such as students, instructors, departments, courses, and more.

The architecture follows a layered approach, separating routing, business logic, and database access.

## Component Diagram

```mermaid
flowchart TD
    ClientTool["Client (curl / Postman)"]

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
        SQLite["SQLite DB (school.db)"]
    end

    ClientTool --> Routes
    Routes --> Services
    Routes --> Utils
    Services --> Utils
    Services --> DB
    DB --> SQLite
```

## Key Components

- Client: Any tool or user agent—like Postman, curl, or a web browser—used to send HTTP requests to the API.
- Flask API Routes: Defines HTTP endpoints (e.g., /students, /courses) that handle requests, parse inputs, and send responses.
- Service Layer: Contains business logic such as data validation, processing rules, and orchestration between routes and the database layer.
- Database Layer: Responsible for executing raw SQL queries or ORM operations to interact with the SQLite database.
- SQLite: The persistent database that stores all application data according to your defined schema.

## Request Flow

```mermaid
sequenceDiagram
    participant Client
    participant Flask as "Flask Route"
    participant Service as "StudentService"
    participant DB as "DB Layer"
    participant SQLite as "SQLite DB"

    Client->>Flask: POST /students
    Flask->>Service: validate & process data
    alt Data valid
        Service->>DB: insert student
        DB->>SQLite: INSERT INTO students (...)
        SQLite-->>DB: OK
        DB-->>Service: success
        Service-->>Flask: return 201 Created
        Flask-->>Client: 201 Created + JSON success response
    else Data invalid / error occurs
        Service-->>Flask: return error message + status code
        Flask-->>Client: Error response (400, 500, etc.) + JSON error message
    end
```

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

- Flask – API framework
- PostgreSQL (Docker container) – Local development
- Azure Database for PostgreSQL – Cloud database (production)
- Docker – Containerization
- Gunicorn – WSGI server
- GitHub Actions – CI for format, test, coverage, and markdown linting
