# School Flask API - WIP

A Flask-based backend API for managing school records including students, courses, instructors, programs, and enrollments. It uses SQLite for lightweight data storage, runs in a Dockerized environment, and includes Pytest for automated testing to ensure code quality.

## Documentation

- [Architecture](docs/architecture.md)
- [DevOps Practice](docs/devops_practices.md)
- [Learning Notes](docs/learning_note.md)

## Features

- Manage core school entities: students, instructors, departments, programs, courses, enrollments, assignments, terms, and course schedules.
- Supports operations for each entity:
  - **Read** (GET)
  - **Add** (POST)
  - **Update** (PUT/PATCH)
  - **Archive** (soft delete, PATCH)
- Archive functionality to keep historical data without permanent deletion.
- Docker support with multi-stage builds for optimized deployment.
- Automated route testing with Pytest.
- Simple SQLite database setup with schema initialization.

## Tech Stack

- **Flask** – API framework  
- **SQLite** – Lightweight relational database  
- **Docker** – Containerization  
- **Pytest** – Testing framework  
- **GitHub Actions** – Continuous Integration (CI)

## API Routes and Supported Operations

| Route             | Read (GET) | Add (POST) | Update (PUT/PATCH) | Archive (PATCH) |
|-------------------|------------|------------|--------------------|-----------------|
| `/assignments`    | ✔          | ✘          | ✘                  | ✘               |
| `/course_schedule`| ✔          | ✘          | ✘                  | ✘               |
| `/courses`        | ✔          | ✘          | ✘                  | ✘               |
| `/departments`    | ✔          | ✘          | ✘                  | ✘               |
| `/enrollments`    | ✔          | ✘          | ✘                  | ✘               |
| `/instructors`    | ✔          | ✘          | ✘                  | ✘               |
| `/programs`       | ✔          | ✘          | ✘                  | ✘               |
| `/students`       | ✔          | ✘          | ✘                  | ✘               |
| `/terms`          | ✔          | ✘          | ✘                  | ✘               |