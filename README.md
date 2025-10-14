# School Flask API

A hands-on project to explore backend development by building a Flask-based REST API for managing school-related data — including students, courses, instructors, and programs. This project is part of my learning journey to better understand how backend systems are structured and how data flows through them.

## 📺 Demo

Check out the YouTube demo to see the API in action:

👉 [Watch the Demo](https://youtube.com/shorts/7JlKnhOzrFE)

**About this video:**

This video demonstrates a Flask REST API deployed on an Azure Web App using Docker, with Azure Container Registry (ACR) for image storage and Azure Database for PostgreSQL for data storage.

**The demo covers:**

- Architecture overview
- Request/response flow
- Example API calls (read, create, update, archive) on instructors

A simple walkthrough of deploying and testing a school database API on Azure.

---

## Tech Stack

![Python](https://img.shields.io/badge/Python-3776AB.svg?style=for-the-badge&logo=Python&logoColor=white) ![Flask](https://img.shields.io/badge/Flask-3BABC3.svg?style=for-the-badge&logo=Flask&logoColor=white) ![PostgreSQL](https://img.shields.io/badge/PostgreSQL-4169E1.svg?style=for-the-badge&logo=PostgreSQL&logoColor=white) ![Azure](https://img.shields.io/badge/Azure-007FFF.svg?style=for-the-badge&logo=Azure&logoColor=white) ![Docker](https://img.shields.io/badge/Docker-2496ED.svg?style=for-the-badge&logo=Docker&logoColor=white) ![Pytest](https://img.shields.io/badge/Pytest-0A9EDC.svg?style=for-the-badge&logo=Pytest&logoColor=white) ![GitHub Actions](https://img.shields.io/badge/GitHub%20Actions-2088FF.svg?style=for-the-badge&logo=GitHub-Actions&logoColor=white)

## Documentation & Notes

- [Architecture Overview](docs/architecture.md)  
- [DevOps Practices](docs/devops_practices.md)  
- [Learning Notes](docs/learning_note.md)  

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

## Environments Overview

This project supports three main environments for development and deployment:

- **Local Development:**
  - Run the Flask API directly on your machine using your own Python environment and a local PostgreSQL instance (optional).
  - Fastest for debugging and iterating on code.

- **Dockerized PostgreSQL (Recommended for Local Dev):**
  - Use Docker Compose to spin up both the Flask API and a PostgreSQL database in containers.
  - Ensures consistency and easy setup—no need to install PostgreSQL locally.
  - Ideal for development and testing.

- **Production (Azure Database for PostgreSQL):**
  - Deploy the Flask API to production and connect to a managed Azure Database for PostgreSQL instance.
  - Provides cloud reliability, backups, and scalability for real-world use.

See below for how to run and configure each environment.

All interactions happen through REST APIs, using tools like curl, Postman, or automated test scripts. There is no frontend.

## 🛠️ Running & Configuring Environments

### 1. Local Development (Direct)

- Install Python and dependencies from `requirements.txt`.
- (Optional) Install PostgreSQL locally and update your environment variables to point to your local DB.
- Run the Flask app directly for fast iteration.

### 2. Local Development (Dockerized PostgreSQL)

- **Recommended:** Use Docker Compose for a consistent, isolated environment.
- Prerequisites: Docker, `make` (most Unix-based systems).
- Start everything with:

  ```sh
  make up
  ```

- Interact with the API (example):

  ```sh
  ./api_client.sh read students
  ```

- Stop and clean up Docker resources:

  ```sh
  make down
  # or
  make down V=1 # clear volume
  ```

### 3. Production (Azure Database for PostgreSQL)

- Deploy the Flask API to your production environment (e.g., Azure App Service, VM, or container).
- Provision an Azure Database for PostgreSQL instance.
- Update your environment variables to point to the Azure DB connection string.
- Run migrations/init scripts as needed (see `scripts/init_azure_db.sh`).

---

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
