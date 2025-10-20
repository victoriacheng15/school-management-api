# 🧭 Learning Notes

Here’s a summary of what I learned while building this Flask API project.

---

## 🧩 Docker Multi-Stage Builds

**Context:** While containerizing my Flask API, I compared single-stage and multi-stage Docker builds to understand performance and image size differences.

**What I Learned:**

- Multi-stage builds produce smaller, cleaner images by separating build dependencies from the runtime environment.  
- The resulting image is more secure and efficient to deploy.  
- For small projects, build-time improvement is minor, but image size and maintainability improve significantly.  

**Why It Matters:**

- Reduces attack surface and unnecessary files in production images.  
- Optimizes CI/CD pipelines and deployment performance.  
- Encourages better separation of concerns between build and runtime stages.  

**How I Applied It:**

- Measured a single-stage build: ~1.67s build time.  
- Measured a multi-stage build: ~1.08s build time.  
- Verified that the multi-stage image excluded build tools and cached files, resulting in a smaller, more focused final image.  

**Challenges / Limitations:**

- Slightly more complex Dockerfile syntax to maintain.  
- Minimal build-time difference for small applications.  

**References:**

- Docker Docs: Multi-Stage Builds  
- Best Practices for Building Efficient Docker Images  

---

## 🧩 Archiving Data

**Context:** While designing the database schema, I explored how production systems manage and archive old or inactive data efficiently.

**What I Learned:**

- Archiving prevents large table growth and improves query performance.  
- Combining `updated_at` with a `status` column provides a reliable way to flag inactive records.  
- Archiving ensures compliance with data retention policies.  

**Why It Matters:**

- Keeps active tables lightweight and responsive.  
- Simplifies reporting by separating current vs. historical data.  
- Helps meet legal or organizational data retention requirements.  

**How I Applied It:**

- Added `is_archived`, `status`, and `updated_at` columns to relevant tables (e.g., `students`, `instructors`).  
- Defined logic to flag records as archived after inactivity (e.g., 1 year).  
- Ensured archived data remains accessible for compliance purposes.  

**Challenges / Limitations:**

- Requires additional maintenance scripts or cron jobs for automated archiving.  
- Queries must explicitly exclude archived records where appropriate.  

**References:**

- Data Archiving Best Practices  
- Efficient Data Management: Overcoming the Challenges of Large Tables with an Archival Strategy  

---

## 🧩 Managing SQLite Database Connections

**Context:** While building the database layer, I investigated safe connection handling patterns for SQLite in API-based applications.

**What I Learned:**

- Closing the database connection after each operation prevents locks and memory issues.  
- Each API call should manage its own short-lived connection.  
- Persistent connections are better suited for larger systems like PostgreSQL or MySQL.  

**Why It Matters:**

- SQLite doesn’t handle concurrent writes well, so keeping connections short-lived avoids contention.  
- Simplifies error recovery and ensures resources are released properly.  

**How I Applied It:**

- Wrapped every query execution in a `try-finally` block.  
- Ensured `self.close()` runs after `execute_query`, `execute_many`, and `execute_script` calls.  
- Verified stability by testing multiple API calls without connection leaks.  

**Challenges / Limitations:**

- Opening and closing connections frequently adds minimal overhead, but is acceptable for small apps.  
- Connection pooling isn’t available by default in SQLite.  

**References:**

- PostgreSQL Connection Pooling  
- Why Connection Pooling Is Essential for Database Optimization  

---

## 🧩 Python Decorators for Exception Handling

**Context:** To make route handlers cleaner and more consistent, I implemented custom decorators to handle exceptions across Flask routes.

**What I Learned:**

- Decorators can abstract repetitive logic such as exception handling, logging, and validation.  
- This pattern improves code maintainability and readability.  
- Centralized error handling helps return consistent API responses.  

**Why It Matters:**

- Reduces repetitive `try-except` blocks in every route.  
- Encourages consistent structure and reusable error patterns.  
- Easier to extend (e.g., add logging or authorization layers later).  

**How I Applied It:**

- Wrote decorators to catch `KeyError` and general exceptions.  
- Returned JSON responses with descriptive error messages and proper HTTP codes.  
- Applied the decorators across multiple route functions.  

**Challenges / Limitations:**

- Requires careful decorator ordering when stacking multiple decorators.  
- Must ensure wrapped functions preserve metadata (using `functools.wraps`).  

**References:**

- Python Docs: functools.wraps  
- Flask Patterns: Centralized Error Handling  

---

## 🧩 The N+1 Problem in Bulk Operations

**Context:** While implementing bulk creation endpoints (students, instructors, courses), I encountered the N+1 query problem.

**What I Learned:**

- Executing inserts one-by-one in a loop causes unnecessary database roundtrips.  
- Batch operations improve efficiency, especially at scale.  
- SQLite’s `executemany()` supports batch inserts but lacks built-in ID retrieval for inserted rows.  

**Why It Matters:**

- Prevents performance bottlenecks during bulk API operations.  
- Enables faster and more scalable data ingestion in production systems.  

**How I Applied It:**

- Used simple one-by-one inserts for this learning project for simplicity.  
- Documented that batch inserts are the preferred pattern for production.  
- Planned a future refactor using `executemany()` plus an additional query to fetch inserted IDs.  

**Challenges / Limitations:**

- SQLite doesn’t easily return multiple inserted IDs in batch mode.  
- Requires restructuring model/service layers to handle batch inserts cleanly.  

**References:**

- Python SQLite executemany Documentation  
- Articles on Solving the N+1 Query Problem  

---

## 🧠 Summary

This project helped me deepen my understanding of containerization, database design, and backend engineering patterns. Each challenge—from managing Docker builds to improving database logic—reinforced how small architectural choices impact performance, maintainability, and scalability.
