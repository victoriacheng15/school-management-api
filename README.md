# School Flask API

A hands-on project to explore backend development by building a Flask-based REST API for managing school-related data — including students, courses, instructors, and programs. This project is part of my learning journey to better understand how backend systems are structured and how data flows through them.

It's built with Flask, SQLite/PostgreSQL, Docker, and includes automated testing, following principles of backend architecture and modern DevOps workflows — with zero frontend.

All interactions happen through REST APIs, using tools like curl, Postman, or automated test scripts.

## Documentation & Notes

- [Architecture Overview](docs/architecture.md)  
- [DevOps Practices](docs/devops_practices.md)  
- [Learning Notes](docs/learning_note.md)  

## Tech Stack

![Python](https://img.shields.io/badge/Python-3776AB.svg?style=for-the-badge&logo=Python&logoColor=white) ![Flask](https://img.shields.io/badge/Flask-3BABC3.svg?style=for-the-badge&logo=Flask&logoColor=white) ![Sqlite](https://img.shields.io/badge/SQLite-003B57.svg?style=for-the-badge&logo=SQLite&logoColor=white) ![PostgreSQL](https://img.shields.io/badge/PostgreSQL-4169E1.svg?style=for-the-badge&logo=PostgreSQL&logoColor=white) ![Docker](https://img.shields.io/badge/Docker-2496ED.svg?style=for-the-badge&logo=Docker&logoColor=white) ![Pytest](https://img.shields.io/badge/Pytest-0A9EDC.svg?style=for-the-badge&logo=Pytest&logoColor=white) ![GitHub Actions](https://img.shields.io/badge/GitHub%20Actions-2088FF.svg?style=for-the-badge&logo=GitHub-Actions&logoColor=white)

## Why I Built This

To gain real backend experience beyond tutorials by:

- Designing clean, modular REST APIs
- Handling CRUD + archive logic across multiple entities
- Writing testable, maintainable backend logic
- Practicing containerization using Docker (incl. multi-stage builds)
- Deploying to a real platform (Render)
- Applying CI/CD and testing best practices
- Includes automated CI/CD workflows using GitHub Actions:
  - Code formatting and linting (Ruff)
  - Unit tests across supported databases (SQLite and PostgreSQL)
  - Coverage reporting with PR comments

## What It Does

- Provides RESTful endpoints for core school entities like students, instructors, courses, and enrollments  
- Supports full CRUD plus archiving (soft deletes) to preserve data history  
- Uses SQLite as an embedded database **within the Docker container** for easy, lightweight local development and testing  
- Fully containerized with Docker (including multi-stage builds) for clean deployment  
- Includes Pytest-based tests covering routes and business logic

## 🛠️ Running Locally

To run this project locally, use Docker Compose for a fast and consistent setup:

### Prerequisites

- Docker
- `make` (built into most Unix-based systems)
- PostgreSQL (optional, if you want to use Postgres locally)

### � Quick Start with Docker Compose

- **Build and start the containers:**

```sh
make up
```

- **Running the script to see if data is returned or not**

```sh
./api_client.sh read students
```

- **Stop and clean up Docker resources:**

```sh
make down
# or 
make down V=1 # clear volume
```

> By default, this uses PostgreSQL. To use Sqlite, set the environment variable `DATABASE_TYPE=sqlite` and ensure your PostgreSQL service is running (see `docker-compose.yml`).

## 🧪 Interact with the API via Bash Script

A helper script `api_client.sh` is included to simplify sending requests to the API without needing Postman or typing full `curl` commands.

### Usage

```bash
./api_client.sh read students
./api_client.sh read students 1
./api_client.sh read students active
./api_client.sh create students
./api_client.sh update students
```

### API Highlights

Supports deployment with either SQLite or PostgreSQL, depending on your environment and needs.

| Resource           | GET | POST | PUT | PATCH (Archive) |
|--------------------|-----|------|-----|-----------------|
| Assignments        | ✔   | ✔    | ✔   | ✔               |
| Course Schedule    | ✔   | ✔    | ✔   | ✔               |
| Courses            | ✔   | ✔    | ✔   | ✔               |
| Departments        | ✔   | ✔    | ✔   | ✔               |
| Enrollments        | ✔   | ✔    | ✔   | ✔               |
| Instructors        | ✔   | ✔    | ✔   | ✔               |
| Programs           | ✔   | ✔    | ✔   | ✔               |
| Students           | ✔   | ✔    | ✔   | ✔               |
| Terms              | ✔   | ✔    | ✔   | ✔               |

