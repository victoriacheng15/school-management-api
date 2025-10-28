# School Management API

A backend and DevOps learning project that simulates a real-world school management system. It started as a simple SQLite prototype and evolved into a Dockerized Flask API connected to Azure Database for PostgreSQL, complete with automated CI/CD and test coverage reporting.

## 📺 Demo

Check out the YouTube demo to see the API in action:

👉 [Watch the Demo](https://www.youtube.com/shorts/B1n6sOdT3PE)

**This short video shows:**

- Architecture overview
- Request/response flow
- Example API calls for instructors (read, create, update, archive)
- Deployment to Azure Web App using Docker and ACR

---

## 🧰 Tech Stack

![Python](https://img.shields.io/badge/Python-3776AB.svg?style=for-the-badge&logo=Python&logoColor=white) ![Flask](https://img.shields.io/badge/Flask-3BABC3.svg?style=for-the-badge&logo=Flask&logoColor=white) ![PostgreSQL](https://img.shields.io/badge/PostgreSQL-4169E1.svg?style=for-the-badge&logo=PostgreSQL&logoColor=white) ![Azure](https://img.shields.io/badge/Azure-007FFF.svg?style=for-the-badge&logo=Azure&logoColor=white) ![Docker](https://img.shields.io/badge/Docker-2496ED.svg?style=for-the-badge&logo=Docker&logoColor=white) ![Pytest](https://img.shields.io/badge/Pytest-0A9EDC.svg?style=for-the-badge&logo=Pytest&logoColor=white) ![GitHub Actions](https://img.shields.io/badge/GitHub%20Actions-2088FF.svg?style=for-the-badge&logo=GitHub-Actions&logoColor=white)

## 📘 Documentation & Notes

- [Architecture Overview](docs/architecture.md): High-level system design and data flow
- [DevOps Practices](docs/devops_practices.md): CI/CD setup, Docker use, Azure integration
- [Learning Notes](docs/learning_note.md): Key lessons, decisions, and trade-offs from the project

## 🧠 Why I Built This

I built this project to gain real backend engineering experience beyond tutorials — focusing on how systems evolve from local development to cloud deployment.

### Goals

- Design clean, modular REST APIs for multiple entities
- Implement CRUD + archiving logic to preserve data history
- Write maintainable and testable backend logic
- Practice containerization using multi-stage Docker builds
- Build automated CI/CD pipelines for linting, testing, and coverage reporting
- Deploy to the cloud with Azure Database for PostgreSQL

### DevOps & Automation

- Continuous integration via GitHub Actions
- Ruff for formatting and linting
- Pytest for unit and integration testing
- Coverage reports automatically posted in pull requests

## ⚙️ What It Does

- Exposes RESTful endpoints for students, instructors, courses, enrollments, and more
- Supports full CRUD + soft-delete (archive) logic
- Uses PostgreSQL (Dockerized locally, Azure-managed in production)
- Fully containerized for consistent deployment
- Includes automated tests for routes and business logic

## 🌍 Environment Overview

This project is designed to simulate real development and deployment environments:

| Environment | Description |
|-------------|-------------|
| **Local (Direct)** | Run Flask API with your local Python env and PostgreSQL. Fastest for debugging. |
| **Local (Dockerized)** | Use Docker Compose to spin up Flask API + PostgreSQL. Reproducible, isolated environment. |
| **Production (Azure)** | Deployed Flask API connected to Azure Database for PostgreSQL. Provides reliability, backups, scalability. |

## 🧪 Running Locally

### 1. Local Development (Direct)

```bash
# Install dependencies
pip install -r requirements.txt
# Run app
python run.py
```

(Optionally, install PostgreSQL locally and configure your `.env`.)

### 2. Local Development (Dockerized) - Recommended

```bash
make up      # start API + DB containers via Docker Compose
./api_client.sh read students
make down    # stop containers
make down V=1  # clear volumes if needed
```

### 3. Production (Azure)

- Deploy Docker image via ACR to Azure Web App
- Connect to Azure Database for PostgreSQL
- Update environment variables and run init scripts (`scripts/init_azure_db.sh`)

---

## � API Highlights

Includes a helper Bash script `api_client.sh` to simplify testing via command line.

```bash
./api_client.sh read students
./api_client.sh create instructors
./api_client.sh archive courses
```

| Resource | GET | POST | PUT | PATCH (Archive) |
|----------|-----|------|-----|-----------------|
| Students | ✔ | ✔ | ✔ | ✔ |
| Instructors | ✔ | ✔ | ✔ | ✔ |
| Courses | ✔ | ✔ | ✔ | ✔ |
| Enrollments | ✔ | ✔ | ✔ | ✔ |
| Programs | ✔ | ✔ | ✔ | ✔ |
| Departments | ✔ | ✔ | ✔ | ✔ |
| Assignments | ✔ | ✔ | ✔ | ✔ |
| Terms | ✔ | ✔ | ✔ | ✔ |

---

## 🧾 Summary

This project evolved from a simple CRUD API into a production-ready backend with:

- Dockerized PostgreSQL
- Automated CI/CD
- Cloud deployment on Azure

It represents a practical journey through backend design, DevOps practices, and system evolution — the way real-world services grow.
