# Learning Notes

Here is a section of what I learned from this project:

## Docker builds

During the development of this Flask API, I compared the build process between **single-stage** and **multi-stage** Dockerfiles. Here are some of the findings:

- Single-stage build:
  - Time taken: Approximately 0.50s
  - Process:
    - All dependencies, including build tools and caches, are installed into the same image.
    - The final image size is larger due to the inclusion of build tools and extra files.
- Multi-Stage Build
  - Time Taken: Approximately 0.32s
  - Process:
    - Dependencies are installed in a separate builder stage, and only the necessary files (like the app and required libraries) are copied into the final image.
    - The final image is smaller and cleaner, containing only the essential runtime environment.
- Conclusion:
  - Multi-Stage Builds are faster and create smaller, cleaner images than single-stage builds.
  - For small apps like this one, the difference in build time might not be significant, but the resulting image size is smaller and more efficient.
  - Multi-stage builds are particularly useful when you want to separate build dependencies from production runtime, reducing security risks and keeping images optimized.

## Archiving Data

While building the database schema for this project, I also learned how real-world apps handle archiving old or inactive data.

- Why archive data?
  - To keep the main tables small and fast.
  - To separate active records from old/inactive ones.
  - To follow data retention rules (e.g., keep inactive student records for one year).
- How archiving usually works:
  - Add an `is_archived` column to tables like students, instructors, or courses.
  - Use the `updated_at` column to track when each record was last changed.
  - Combine `updated_at` with a status field (like the `status` column in the students table) to decide whether a record is inactive.
  - If a student has an inactive status and hasn’t been updated for a long time (e.g., one year), the record can be marked as archived or moved to an archive table.
- What I learned:
  - Archiving based on `updated_at` along with the record’s status is a more accurate approach.
  - It helps reduce clutter and keeps recent data easy to access.
  - Users like students aren’t archived immediately — they are given time before being flagged.
- Sources I referenced:
  - [Data archiving best practice](https://success.outsystems.com/documentation/outsystems_developer_cloud/building_apps/data_management/best_practices_for_data_management/data_archiving_best_practice)
  - [Efficient Data Management: Overcoming the Challenges of Large Tables with an Archival Strategy](https://opensource-db.com/efficient-data-management-overcoming-the-challenges-of-large-tables-with-an-archival-strategy)
  
## Database Connection

While building the database layer for this project, I explored how to manage SQLite connections in a clean and safe way.

- Why close the database connection after each operation?
  - Prevents database locks and memory issues, especially in SQLite.
  - Ensures connections aren’t left open accidentally.
  - Each API call is independent, so there’s no need to keep the connection open.
- How I applied it:
  - Updated the Database class to call self.close() in a finally block after every execute_query, execute_many, and execute_script call.
  - This guarantees the connection is closed, even if an error happens during execution.
- What I learned:
  - For SQLite, it’s generally better to open and close the connection for each operation to avoid issues and keep things simple.
  - In larger SQL databases (like PostgreSQL or MySQL), keeping a persistent connection (e.g., using connection pooling) is more common for performance.
    - sources:
      - [PostgreSQL Connection Pooling](https://www.compilenrun.com/docs/database/postgresql/postgresql-best-practices/postgresql-connection-pooling/?utm_source=chatgpt.com)
      - [Why Connection Pooling Is Essential for PostgreSQL Database Optimisation](https://caw.tech/why-connection-pooling-is-essential-for-postgresql-database-optimisation/)
  - Since this is a small app using SQLite, closing the connection after each use is a good, safe choice.

## Python Decorators for Exception Handling

To improve route code readability and reduce repetitive error handling in the Flask API, I wrote custom Python decorators.

- Why use decorators for exception handling?
  - They allow wrapping route functions to automatically catch and handle common errors.
  - They reduce boilerplate try-except blocks scattered across multiple routes.
  - Improve consistency in error responses returned by the API.
- How I applied it:
  - Created decorators that catch specific exceptions like `KeyError` and general exceptions.
  - Decorators return JSON error responses with proper HTTP status codes.
  - Applied these decorators across route handlers to keep route logic clean and focused on core functionality.
- What I learned:
  - Decorators are a powerful Python feature to abstract cross-cutting concerns like error handling.
  - Simplifying routes this way makes the code easier to maintain and extend.
  - This pattern can be reused for logging, authorization checks, or input validation in future projects.

## N+1 Problem in Bulk Operations

While implementing bulk creation endpoints in this API (for students, instructors, courses, etc.), I encountered the classic N+1 problem.

- Why is it a problem?
  - The current approach inserts each entity one by one in a loop, resulting in a separate database query for each record.
  - This is inefficient for large batches, as it increases database load and slows down API response times.

- How I handled it in this project:
  - For simplicity and because this is a sandbox project, I kept the one-by-one insert logic for all bulk creation routes.
  - I noted that SQLite’s `executemany` can be used for batch inserts, but it does not easily return all inserted row IDs.
  - Fixing this would require refactoring the service and model layers to support batch inserts and fetching all inserted IDs for the response.

- What I learned:
  - The N+1 problem is a common performance issue in APIs that process bulk operations.
  - Batch inserts (using methods like `executemany`) are the recommended solution, but may require additional logic to retrieve all inserted IDs.
  - For production systems, it’s important to avoid N+1 patterns to ensure scalability and efficiency.

- What I would do in a production app:
  - Implement a batch insert function in the model layer using `executemany` for all bulk creation endpoints.
  - Refactor the service/helper logic to use the batch insert and fetch all inserted IDs for the response, possibly by querying with a unique field or timestamp after the insert.

- Sources I referenced:
  - [Python SQLite executemany docs](https://docs.python.org/3/library/sqlite3.html#sqlite3.Cursor.executemany)
