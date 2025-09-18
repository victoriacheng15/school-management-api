# School Flask API

A hands-on project to explore backend development by building a Flask-based REST API for managing school-related data — including students, courses, instructors, and programs. This project is part of my learning journey to better understand how backend systems are structured and how data flows through them.

It's built with Flask, PostgreSQL, Docker, and includes automated testing, following principles of backend architecture and modern DevOps workflows — with zero frontend.

All interactions happen through REST APIs, using tools like curl, Postman, or automated test scripts.

## Documentation & Notes

- [Architecture Overview](docs/architecture.md)  
- [DevOps Practices](docs/devops_practices.md)  
- [Learning Notes](docs/learning_note.md)  

## Tech Stack

![Python](https://img.shields.io/badge/Python-3776AB.svg?style=for-the-badge&logo=Python&logoColor=white) ![Flask](https://img.shields.io/badge/Flask-3BABC3.svg?style=for-the-badge&logo=Flask&logoColor=white) ![PostgreSQL](https://img.shields.io/badge/PostgreSQL-4169E1.svg?style=for-the-badge&logo=PostgreSQL&logoColor=white) ![Azure](https://img.shields.io/badge/Azure-007FFF.svg?style=for-the-badge&logo=Azure&logoColor=white) ![Docker](https://img.shields.io/badge/Docker-2496ED.svg?style=for-the-badge&logo=Docker&logoColor=white) ![Pytest](https://img.shields.io/badge/Pytest-0A9EDC.svg?style=for-the-badge&logo=Pytest&logoColor=white) ![GitHub Actions](https://img.shields.io/badge/GitHub%20Actions-2088FF.svg?style=for-the-badge&logo=GitHub-Actions&logoColor=white)

## Why I Built This

To gain real backend experience beyond tutorials by:

- Designing clean, modular REST APIs
- Handling CRUD + archive logic across multiple entities
- Writing testable, maintainable backend logic
- Practicing containerization using Docker (incl. multi-stage builds)
- Implementing automated CI/CD pipelines for code quality and testing
- Expanding to use Azure Database for PostgreSQL for production/cloud experience
- Utilizing Dockerized PostgreSQL for local development and testing
- Includes automated CI/CD workflows using GitHub Actions:
  - Code formatting and linting (Ruff)
  - Unit tests
  - Coverage reporting with PR comments

## What It Does

- Provides RESTful endpoints for core school entities (students, instructors, courses, enrollments, etc.)
- Supports full CRUD operations plus archiving (soft deletes) to preserve data history
- Uses PostgreSQL for robust, production-ready data management (local via Docker, cloud via Azure)
- Is fully containerized for easy deployment
- Includes automated tests for routes and business logic

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

Uses PostgreSQL for robust data management and production-ready deployment.

| Resource           | GET (Read) | POST (Create) | PUT (Update) | PATCH (Archive) |
|--------------------|------------|---------------|--------------|-----------------|
| Assignments        | ✔          | ✔             | ✔            | ✔               |
| Course Schedule    | ✔          | ✔             | ✔            | ✔               |
| Courses            | ✔          | ✔             | ✔            | ✔               |
| Departments        | ✔          | ✔             | ✔            | ✔               |
| Enrollments        | ✔          | ✔             | ✔            | ✔               |
| Instructors        | ✔          | ✔             | ✔            | ✔               |
| Programs           | ✔          | ✔             | ✔            | ✔               |
| Students           | ✔          | ✔             | ✔            | ✔               |
| Terms              | ✔          | ✔             | ✔            | ✔               |
