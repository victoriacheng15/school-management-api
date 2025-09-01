# Progress Report: School Flask API Database Migration

**Date:** September 1, 2025

## Overview

Migrating from SQLite to PostgreSQL, with dual support during the transition. Each route is being updated to ensure models, services, and tests work with PostgreSQL.

## Current Status

- Dual database support in place.
- Student route fully migrated (models, services, tests).
- PostgreSQL setup and Docker integration complete.
- Migration scripts and schema for PostgreSQL ready.

## Migration Checklist by Route

### Students

- [x] Models updated for PostgreSQL
- [x] Services support PostgreSQL
- [x] Tests run with PostgreSQL

### Instructors

- [ ] Models updated for PostgreSQL
- [ ] Services support PostgreSQL
- [ ] Tests run with PostgreSQL

### Courses

- [ ] Models updated for PostgreSQL
- [ ] Services support PostgreSQL
- [ ] Tests run with PostgreSQL

### Departments

- [ ] Models updated for PostgreSQL
- [ ] Services support PostgreSQL
- [ ] Tests run with PostgreSQL

### Programs

- [ ] Models updated for PostgreSQL
- [ ] Services support PostgreSQL
- [ ] Tests run with PostgreSQL

### Enrollments

- [ ] Models updated for PostgreSQL
- [ ] Services support PostgreSQL
- [ ] Tests run with PostgreSQL

### Assignments

- [ ] Models updated for PostgreSQL
- [ ] Services support PostgreSQL
- [ ] Tests run with PostgreSQL

### Terms

- [ ] Models updated for PostgreSQL
- [ ] Services support PostgreSQL
- [ ] Tests run with PostgreSQL

### Course Schedules

- [ ] Models updated for PostgreSQL
- [ ] Services support PostgreSQL
- [ ] Tests run with PostgreSQL

## General Tasks

- [x] PostgreSQL schema and migration scripts
- [x] Docker integration for PostgreSQL
- [ ] Remove SQLite dependencies and code
- [ ] Update documentation

## Next Steps

- Continue migrating each route (models, services, tests) to PostgreSQL.
- Complete testing for all features.
- Remove SQLite and update documentation.
