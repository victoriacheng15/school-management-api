# School Flask API — A Personal Project for Learning Backend Development

This is a personal, hands-on project to build a comprehensive backend API for managing school data — students, courses, instructors, programs, and more. It’s designed as a fun but challenging way to deepen my skills in Flask, database management, Docker, and test automation.

This is a **backend-only project** — there’s no frontend. All interactions are done through RESTful APIs, automated tests, and external tools like Postman or `curl`.

## Documentation & Notes

- [Architecture Overview](docs/architecture.md)  
- [DevOps Practices](docs/devops_practices.md)  
- [Learning Notes](docs/learning_note.md)  

## Tech Stack

![Python](https://img.shields.io/badge/Python-3776AB.svg?style=for-the-badge&logo=Python&logoColor=white) ![Flask](https://img.shields.io/badge/Flask-3BABC3.svg?style=for-the-badge&logo=Flask&logoColor=white) ![Sqlite](https://img.shields.io/badge/SQLite-003B57.svg?style=for-the-badge&logo=SQLite&logoColor=white) ![Docker](https://img.shields.io/badge/Docker-2496ED.svg?style=for-the-badge&logo=Docker&logoColor=white) ![Pytest](https://img.shields.io/badge/Pytest-0A9EDC.svg?style=for-the-badge&logo=Pytest&logoColor=white) ![GitHub Actions](https://img.shields.io/badge/GitHub%20Actions-2088FF.svg?style=for-the-badge&logo=GitHub-Actions&logoColor=white)

## Why I Built This

Building a realistic, multi-entity backend API is a great way to practice:

- Designing clean, modular backend architectures  
- Handling CRUD and soft-delete operations across related resources  
- Writing automated tests to ensure code correctness  
- Using Docker to containerize and deploy applications  
- Managing SQLite databases without heavy ORM layers  
- Gaining confidence deploying backend services to cloud platforms

This project is a playground for applying best practices I’m learning and improving my understanding of backend systems from end to end.

## What It Does

- Provides RESTful endpoints for core school entities like students, instructors, courses, and enrollments  
- Supports full CRUD plus archiving (soft deletes) to preserve data history  
- Uses SQLite as an embedded database **within the Docker container** for easy, lightweight local development and testing  
- Fully containerized with Docker (including multi-stage builds) for clean deployment  
- Deployed on Render, demonstrating real-world backend deployment experience  
- Includes Pytest-based tests covering routes and business logic  


## API Highlights

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
