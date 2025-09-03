#!/usr/bin/env python3
"""
PostgreSQL Database Initialization Script
This script initializes the PostgreSQL database with the schema and sample data.
"""

import os
import sys

sys.path.append(".")

from db.database import Database


def init_postgresql_database():
    """Initialize PostgreSQL database with schema"""
    print("Initializing PostgreSQL database...")

    # Use environment variables already set by docker-compose
    # No need to override them here

    try:
        db = Database()

        # Read and execute PostgreSQL schema
        with open("db/schema_postgresql.sql", "r") as f:
            schema_sql = f.read()

        # Execute the schema
        db.execute_script(schema_sql)
        print("✅ PostgreSQL schema created successfully!")

        # Verify tables were created
        tables_query = """
        SELECT table_name 
        FROM information_schema.tables 
        WHERE table_schema = 'public' 
        AND table_type = 'BASE TABLE'
        ORDER BY table_name;
        """

        tables = db.execute_query(tables_query)
        print(f"\n📋 Created tables:")
        for table in tables:
            print(f"  - {table['table_name']}")

        return True

    except Exception as e:
        print(f"❌ Error initializing PostgreSQL database: {e}")
        return False


def populate_sample_data():
    """Populate PostgreSQL database with sample data"""
    print("\n🌱 Populating sample data...")

    try:
        db = Database()
        from db.data import (
            departments,
            programs,
            instructors,
            terms,
            courses,
            students,
            enrollments,
            assignments,
            course_schedule,
        )

        # Insert departments (convert boolean)
        departments_pg = [
            tuple(bool(v) if i == 4 else v for i, v in enumerate(row))
            for row in departments
        ]
        db.execute_many(
            "INSERT INTO departments (id, name, created_at, updated_at, is_archived) VALUES (%s, %s, %s, %s, %s)",
            departments_pg,
        )

        db.execute_query(
            "SELECT setval('departments_id_seq', (SELECT MAX(id) FROM departments));"
        )

        # Insert programs (convert boolean)
        programs_pg = [
            tuple(bool(v) if i == 6 else v for i, v in enumerate(row))
            for row in programs
        ]
        db.execute_many(
            "INSERT INTO programs (id, name, type, department_id, created_at, updated_at, is_archived) VALUES (%s, %s, %s, %s, %s, %s, %s)",
            programs_pg,
        )

        db.execute_query(
            "SELECT setval('programs_id_seq', (SELECT MAX(id) FROM programs));"
        )

        # Insert instructors (convert boolean)
        instructors_pg = [
            tuple(bool(v) if i == 11 else v for i, v in enumerate(row))
            for row in instructors
        ]
        db.execute_many(
            "INSERT INTO instructors (id, first_name, last_name, email, address, province, employment, status, department_id, created_at, updated_at, is_archived) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
            instructors_pg,
        )

        db.execute_query(
            "SELECT setval('instructors_id_seq', (SELECT MAX(id) FROM instructors));"
        )

        # Insert terms
        db.execute_many(
            "INSERT INTO terms (id, name, start_date, end_date, created_at, updated_at) VALUES (%s, %s, %s, %s, %s, %s)",
            terms,
        )

        db.execute_query(
            "SELECT setval('terms_id_seq', (SELECT MAX(id) FROM terms));"
        )

        # Insert courses (convert boolean)
        courses_pg = [
            tuple(bool(v) if i == 7 else v for i, v in enumerate(row))
            for row in courses
        ]
        db.execute_many(
            "INSERT INTO courses (id, title, code, term_id, department_id, created_at, updated_at, is_archived) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)",
            courses_pg,
        )

        db.execute_query(
            "SELECT setval('courses_id_seq', (SELECT MAX(id) FROM courses));"
        )

        # Insert students (convert Python bools to PostgreSQL bools, force is_archived to False)
        # Map sample data to match SQLite schema structure
        students_pg = [
            tuple(
                list(row[:10])  # First 10 fields (id through status)
                + [bool(row[10])]  # coop (convert to bool)
                + [bool(row[11])]  # is_international (convert to bool)
                + [row[12]]  # program_id
                + list(row[13:15])  # created_at, updated_at
                + [False]  # is_archived (force to False)
            )
            for row in students
        ]
        db.execute_many(
            "INSERT INTO students (id, first_name, last_name, email, address, city, province, country, address_type, status, coop, is_international, program_id, created_at, updated_at, is_archived) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
            students_pg,
        )

        # Reset students sequence to max ID after inserting with explicit IDs
        db.execute_query(
            "SELECT setval('students_id_seq', (SELECT MAX(id) FROM students));"
        )

        # Insert enrollments
        db.execute_many(
            "INSERT INTO enrollments (id, student_id, course_id, grade, created_at, updated_at) VALUES (%s, %s, %s, %s, %s, %s)",
            enrollments,
        )

        # Insert assignments (convert boolean)
        assignments_pg = [
            tuple(bool(v) if i == 5 else v for i, v in enumerate(row))
            for row in assignments
        ]
        db.execute_many(
            "INSERT INTO assignments (id, instructor_id, course_id, created_at, updated_at, is_archived) VALUES (%s, %s, %s, %s, %s, %s)",
            assignments_pg,
        )

        db.execute_query(
            "SELECT setval('assignments_id_seq', (SELECT MAX(id) FROM assignments));"
        )

        # Insert course_schedule (convert boolean)
        course_schedule_pg = [
            tuple(bool(v) if i == 7 else v for i, v in enumerate(row))
            for row in course_schedule
        ]
        db.execute_many(
            "INSERT INTO course_schedule (id, course_id, day, time, room, created_at, updated_at, is_archived) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)",
            course_schedule_pg,
        )

        db.execute_query(
            "SELECT setval('course_schedule_id_seq', (SELECT MAX(id) FROM course_schedule));"
        )

        print("✅ Sample data populated successfully!")
        return True

    except Exception as e:
        print(f"❌ Error populating sample data: {e}")
        return False


if __name__ == "__main__":
    print("PostgreSQL Database Setup")
    print("=" * 40)

    # Initialize schema
    schema_ok = init_postgresql_database()

    if schema_ok:
        # Populate sample data
        data_ok = populate_sample_data()

        if data_ok:
            print("\n🎉 PostgreSQL database setup complete!")
            sys.exit(0)
        else:
            print("\n⚠️  Schema created but sample data failed")
            sys.exit(1)
    else:
        print("\n❌ Database initialization failed")
        sys.exit(1)
