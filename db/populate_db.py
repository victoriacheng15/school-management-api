import os
import logging
from database import Database
from data import (
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

logging.basicConfig(
    format="%(asctime)s - %(levelname)s - %(message)s",
    level=logging.INFO,
    handlers=[
        logging.StreamHandler()
        # Optionally, you can log to a file by adding a file handler
        # logging.FileHandler('db_init.log')  # Uncomment to log to a file
    ],
)

logger = logging.getLogger(__name__)


def populate_db():
    db = Database()
    db.connect()

    # Insert departments
    db.execute_many(
        "INSERT INTO departments (id, name, created_at, updated_at, is_archived) VALUES (?, ?, ?, ?, ?);",
        departments,
    )

    # Insert programs
    db.execute_many(
        "INSERT INTO programs (id, name, type, department_id, created_at, updated_at, is_archived) VALUES (?, ?, ?, ?, ?, ?, ?);",
        programs,
    )

    # Insert instructors
    db.execute_many(
        "INSERT INTO instructors (id, first_name, last_name, email, address, province, employment, status, department_id, created_at, updated_at, is_archived) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);",
        instructors,
    )

    # Insert terms
    db.execute_many(
        "INSERT INTO terms (id, name, start_date, end_date, created_at, updated_at) VALUES (?, ?, ?, ?, ?, ?);",
        terms,
    )

    # Insert courses
    db.execute_many(
        "INSERT INTO courses (id, title, code, term_id, department_id, created_at, updated_at, is_archived) VALUES (?, ?, ?, ?, ?, ?, ?, ?);",
        courses,
    )

    # Insert students
    db.execute_many(
        "INSERT INTO students (id, first_name, last_name, email, address, city, province, country, address_type, status, coop, is_international, program_id, created_at, updated_at, is_archived) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);",
        students,
    )

    # Insert enrollments
    db.execute_many(
        "INSERT INTO enrollments (id, student_id, course_id, grade, created_at, updated_at) VALUES (?, ?, ?, ?, ?, ?);",
        enrollments,
    )

    # Insert assignments
    db.execute_many(
        "INSERT INTO assignments (id, instructor_id, course_id, created_at, updated_at, is_archived) VALUES (?, ?, ?, ?, ?, ?);",
        assignments,
    )

    # Insert course schedules
    db.execute_many(
        "INSERT INTO course_schedule (id, course_id, day, time, room, created_at, updated_at, is_archived) VALUES (?, ?, ?, ?, ?, ?, ?, ?);",
        course_schedule,
    )

    db.close()


if __name__ == "__main__":
    populate_db()
