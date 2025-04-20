import sqlite3
import os
from data import departments, programs, instructors, terms, courses, students, enrollments, assignments, course_schedule


def populate_db():
    db_path = os.path.join("db", "school.db")
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Insert departments
    cursor.executemany(
        "INSERT INTO departments (id, name, created_at, updated_at) VALUES (?, ?, ?, ?);",
        departments,
    )

    # Insert programs
    cursor.executemany(
        "INSERT INTO programs (id, name, type, department_id, created_at, updated_at) VALUES (?, ?, ?, ?, ?, ?);",
        programs,
    )

    # Insert instructors
    
    cursor.executemany(
        "INSERT INTO instructors (id, first_name, last_name, email, address, province, employment, status, department_id, created_at, updated_at) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);",
        instructors,
    )

    # Insert terms

    cursor.executemany(
        "INSERT INTO terms (id, name, start_date, end_date, created_at, updated_at) VALUES (?, ?, ?, ?, ?, ?);",
        terms,
    )

    # Insert courses

    cursor.executemany(
        "INSERT INTO courses (id, title, code, term_id, department_id, created_at, updated_at) VALUES (?, ?, ?, ?, ?, ?, ?);",
        courses,
    )

    # Insert students
    
    cursor.executemany(
        "INSERT INTO students (id, first_name, last_name, email, address, province_state, country, address_type, status, coop, is_international, program_id, created_at, updated_at) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);",
        students,
    )

    # Insert enrollments

    cursor.executemany(
        "INSERT INTO enrollments (id, student_id, course_id, grade, created_at, updated_at) VALUES (?, ?, ?, ?, ?, ?);",
        enrollments,
    )

    # Insert assignments

    cursor.executemany(
        "INSERT INTO assignments (id, instructor_id, course_id, created_at, updated_at) VALUES (?, ?, ?, ?, ?);",
        assignments,
    )

    # Insert course schedule

    cursor.executemany(
        "INSERT INTO course_schedule (id, course_id, day, time, room, created_at, updated_at) VALUES (?, ?, ?, ?, ?, ?, ?);",
        course_schedule,
    )

    conn.commit()
    conn.close()


if __name__ == "__main__":
    populate_db()
