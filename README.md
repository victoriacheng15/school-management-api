# School Flask API — A Personal Project for Learning Backend Development

A hands-on project to explore backend development by building a Flask-based REST API for managing school-related data — including students, courses, instructors, and programs. This project is part of my learning journey to better understand how backend systems are structured and how data flows through them.

It's built with Flask, SQLite, Docker, and includes automated testing, following principles of backend architecture and modern DevOps workflows — with zero frontend.

All interactions happen through REST APIs, using tools like curl, Postman, or automated test scripts.

## Documentation & Notes

- [Architecture Overview](docs/architecture.md)  
- [DevOps Practices](docs/devops_practices.md)  
- [Learning Notes](docs/learning_note.md)  

## Tech Stack

![Python](https://img.shields.io/badge/Python-3776AB.svg?style=for-the-badge&logo=Python&logoColor=white) ![Flask](https://img.shields.io/badge/Flask-3BABC3.svg?style=for-the-badge&logo=Flask&logoColor=white) ![Sqlite](https://img.shields.io/badge/SQLite-003B57.svg?style=for-the-badge&logo=SQLite&logoColor=white) ![Docker](https://img.shields.io/badge/Docker-2496ED.svg?style=for-the-badge&logo=Docker&logoColor=white) ![Pytest](https://img.shields.io/badge/Pytest-0A9EDC.svg?style=for-the-badge&logo=Pytest&logoColor=white) ![GitHub Actions](https://img.shields.io/badge/GitHub%20Actions-2088FF.svg?style=for-the-badge&logo=GitHub-Actions&logoColor=white)

## Why I Built This

To gain real backend experience beyond tutorials by:

- Designing clean, modular REST APIs  
- Handling CRUD + archive logic across multiple entities  
- Writing testable, maintainable backend logic  
- Practicing containerization using Docker (incl. multi-stage builds)  
- Managing databases without relying on heavy ORMs  
- Deploying to a real platform (Render)  
- Applying CI/CD and testing best practices  

## What It Does

- Provides RESTful endpoints for core school entities like students, instructors, courses, and enrollments  
- Supports full CRUD plus archiving (soft deletes) to preserve data history  
- Uses SQLite as an embedded database **within the Docker container** for easy, lightweight local development and testing  
- Fully containerized with Docker (including multi-stage builds) for clean deployment  
- Deployed on Render, demonstrating real-world backend deployment experience  
- Includes Pytest-based tests covering routes and business logic

## 🛠️ Running Locally

To run this project locally using Docker and `make`:

### Prerequisites
- Python 3.x
- Docker
- `make` (built into most Unix-based systems)

### 🔧 Option 1: Local Python Environment

1. **Create and activate a virtual environment**:

```
python3 -m venv env
source env/bin/activate
```

2. **Install Python dependencies**:

```
make install
```

3. **Initialize the database**:

```
make setup-db
```

4. **Run the app**:

```
python3 run.py
```

The API will be available at [http://localhost:5000](http://localhost:5000)

### 🐳 Option 2: Run with Docker (Recommended)

1. **Start the app using Docker Compose**:

```
make up
```

2. **(Optional) Enter the Docker container** if you want to run tools like `api_client.sh` from inside:

```
docker exec -it school-flask-api /bin/bash
```

Then inside the container, you can run:

```
./api_client.sh read students
```

3. **To stop and clean up Docker resources**:

```
make down
```

> ⚠️ **Note:**  
> You can reset the database at any time (clear all data and re-initialize) by running:  
> 
> ```
> make reset
> ```
>
> This is useful if you want to start fresh without rebuilding containers or reinstalling dependencies.

## 🧪 Interact with the API via Bash Script

A helper script is included to simplify sending requests to the API without needing Postman or typing full `curl` commands.

### Usage

```bash
./api_client.sh read students            # Get all students
./api_client.sh read students 1          # Get student with ID 1
./api_client.sh read students active     # Get active students

./api_client.sh create students          # POST data from create_students variable
./api_client.sh update students          # PUT data from update_students variable
./api_client.sh archive students         # PATCH data from archive_students variable
```

### API Highlights

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


## 🚀 Deployment

The API is containerized using Docker and deployed on [Render](https://render.com) using a Docker deployment method.  
This mimics real-world deployment pipelines and helps reinforce DevOps practices.

> ⚠️ The live instance is private to avoid misuse, since the API currently does not include authentication or rate limiting.

