# School Flask API — A Personal Project for Learning Backend Development

This is a personal, hands-on project to build a comprehensive backend API for managing school data — students, courses, instructors, programs, and more. It’s designed as a fun but challenging way to deepen my skills in Flask, database management, Docker, and test automation.

---

## Why I Built This

Building a realistic, multi-entity API is a great way to practice:

- Designing clean, modular backend architectures  
- Handling CRUD and soft-delete operations across related resources  
- Writing automated tests to ensure code correctness  
- Using Docker to containerize and deploy applications  
- Managing SQLite databases without heavy ORM layers

This project is a playground for applying best practices I’m learning and improving my understanding of backend systems from end to end.

---

## What It Does

- Provides RESTful endpoints for core school entities like students, instructors, courses, and enrollments  
- Supports full CRUD plus archiving (soft deletes) to preserve data history  
- Uses SQLite as an embedded database **within the Docker container** for easy, lightweight local development and testing  
- Fully containerized with Docker (including multi-stage builds) for clean deployment  
- Deployed on Render, demonstrating real-world cloud deployment experience  
- Includes Pytest-based tests covering routes and business logic  

### Documentation & Notes

- [Architecture Overview](docs/architecture.md)  
- [DevOps Practices](docs/devops_practices.md)  
- [Learning Notes](docs/learning_note.md)  

---

## Tech Stack

| Technology     | Purpose                      |
|----------------|------------------------------|
| Flask          | Lightweight web framework    |
| SQLite         | Simple relational database   |
| Docker         | Containerization             |
| Pytest         | Testing framework            |
| GitHub Actions | CI/CD automation             |

---

## API Highlights

| Resource           | GET | POST | PUT | PATCH (Archive) |
|--------------------|-----|------|-----|-----------------|
| Assignments        | ✔   | ✘    | ✘   | ✘               |
| Course Schedule    | ✔   | ✘    | ✘   | ✘               |
| Courses            | ✔   | ✔    | ✔   | ✔               |
| Departments        | ✔   | ✔    | ✔   | ✔               |
| Enrollments        | ✔   | ✘    | ✘   | ✘               |
| Instructors        | ✔   | ✔    | ✔   | ✔               |
| Programs           | ✔   | ✔    | ✔   | ✔               |
| Students           | ✔   | ✔    | ✔   | ✔               |
| Terms              | ✔   | ✔    | ✔   | ✔               |
