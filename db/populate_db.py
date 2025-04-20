import sqlite3
import os
from datetime import datetime

def populate_db():
    db_path = os.path.join("db", "school.db")
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    # Insert departments
    departments = [
        (1, 'Computer Science', now, now),
        (2, 'Cybersecurity', now, now),
        (3, 'Software Engineering', now, now)
    ]
    cursor.executemany("INSERT INTO departments (id, name, created_at, updated_at) VALUES (?, ?, ?, ?);", departments)

    # Insert programs
    programs = [
        (1, 'Computer Science', 'bachelor', 1, now, now),
        (2, 'Cybersecurity', 'diploma', 2, now, now),
        (3, 'Cloud Security', 'certificate', 2, now, now),
        (4, 'Software Development', 'bachelor', 3, now, now)
    ]
    cursor.executemany("INSERT INTO programs (id, name, type, department_id, created_at, updated_at) VALUES (?, ?, ?, ?, ?, ?);", programs)

    # Insert instructors
    instructors = [
        (1, 'Ada', 'Lovelace', 'ada@school.edu', '123 CS Lane', 'London', 'full-time', 'active', 1, now, now),
        (2, 'Alan', 'Turing', 'alan@school.edu', '456 Crypto Ave', 'London', 'adjunct', 'active', 2, now, now),
        (3, 'Grace', 'Hopper', 'grace@school.edu', '789 Compiler Rd', 'New York', 'full-time', 'active', 1, now, now),
        (4, 'Donald', 'Knuth', 'donald@school.edu', '321 Algorithm St', 'California', 'part-time', 'active', 1, now, now),
        (5, 'Barbara', 'Liskov', 'barbara@school.edu', '654 OOP Blvd', 'Massachusetts', 'full-time', 'active', 3, now, now)
    ]
    cursor.executemany("INSERT INTO instructors (id, first_name, last_name, email, address, province, employment, status, department_id, created_at, updated_at) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);", instructors)

    # Insert terms
    terms = [
        (1, 'Fall 2024', '2024-09-01', '2024-12-20', now, now),
        (2, 'Winter 2025', '2025-01-10', '2025-04-30', now, now)
    ]
    cursor.executemany("INSERT INTO terms (id, name, start_date, end_date, created_at, updated_at) VALUES (?, ?, ?, ?, ?, ?);", terms)

    # Insert courses
    courses = [
        (1, 'Introduction to Programming', 'CS101', 1, 1, now, now),
        (2, 'Network Security Basics', 'CY201', 1, 2, now, now),
        (3, 'Advanced Algorithms', 'CS301', 2, 1, now, now),
        (4, 'Cloud Infrastructure', 'CL101', 2, 2, now, now),
        (5, 'Software Design Principles', 'SE202', 2, 3, now, now)
    ]
    cursor.executemany("INSERT INTO courses (id, title, code, term_id, department_id, created_at, updated_at) VALUES (?, ?, ?, ?, ?, ?, ?);", courses)

    # Insert students
    students = [
        (1, 'Alice', 'Wong', 'alice@school.edu', '123 Maple St', 'AB', 'Canada', 'local', 'active', True, False, 1, now, now),
        (2, 'Bob', 'Smith', 'bob@school.edu', '456 Oak St', 'BC', 'Canada', 'permanent', 'active', False, False, 1, now, now),
        (3, 'Charlie', 'Kim', 'charlie@school.edu', '789 Pine St', 'ON', 'Canada', 'local', 'active', True, True, 2, now, now),
        (4, 'Diana', 'Lopez', 'diana@school.edu', '321 Birch St', 'QC', 'Canada', 'local', 'inactive', False, True, 3, now, now),
        (5, 'Evan', 'Brown', 'evan@school.edu', '654 Cedar St', 'NS', 'Canada', 'permanent', 'active', False, False, 1, now, now),
        (6, 'Fay', 'Zhao', 'fay@school.edu', '987 Spruce St', 'AB', 'Canada', 'local', 'active', True, True, 4, now, now),
        (7, 'George', 'Tanaka', 'george@school.edu', '246 Elm St', 'MB', 'Canada', 'permanent', 'active', False, False, 2, now, now),
        (8, 'Hannah', 'Nguyen', 'hannah@school.edu', '135 Fir St', 'SK', 'Canada', 'local', 'active', True, True, 3, now, now),
        (9, 'Isaac', 'Lee', 'isaac@school.edu', '753 Ash St', 'NB', 'Canada', 'local', 'inactive', False, False, 4, now, now),
        (10, 'Julia', 'Martinez', 'julia@school.edu', '159 Hemlock St', 'PE', 'Canada', 'permanent', 'active', True, False, 1, now, now)
    ]
    cursor.executemany("INSERT INTO students (id, first_name, last_name, email, address, province_state, country, address_type, status, coop, is_international, program_id, created_at, updated_at) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);", students)

    # Insert enrollments
    enrollments = [
      (1, 1, 1, 'A', now, now),
      (2, 2, 1, 'B+', now, now),
      (3, 3, 2, 'A-', now, now),
      (4, 4, 3, 'B', now, now),
      (5, 5, 4, 'C+', now, now),
      (6, 6, 5, 'A', now, now),
      (7, 7, 2, 'B-', now, now),
      (8, 8, 3, 'A', now, now),
      (9, 9, 4, 'C', now, now),
      (10, 10, 5, 'B+', now, now)
    ]
    cursor.executemany("INSERT INTO enrollments (id, student_id, course_id, grade, created_at, updated_at) VALUES (?, ?, ?, ?, ?, ?);", enrollments)

    # Insert assignments
    assignments = [
        (1, 1, 1, now, now),  # Ada teaches CS101
        (2, 2, 2, now, now),  # Alan teaches CY201
        (3, 3, 3, now, now),  # Grace teaches CS301
        (4, 4, 4, now, now),  # Donald teaches CL101
        (5, 5, 5, now, now)   # Barbara teaches SE202
    ]
    cursor.executemany("INSERT INTO assignments (id, instructor_id, course_id, created_at, updated_at) VALUES (?, ?, ?, ?, ?);", assignments)

    # Insert course schedule
    course_schedule = [
        (1, 1, 'Monday', '10:00 AM', 'Room 101', now, now),
        (2, 2, 'Tuesday', '2:00 PM', 'Room 102', now, now),
        (3, 3, 'Wednesday', '1:00 PM', 'Room 103', now, now),
        (4, 4, 'Thursday', '3:00 PM', 'Room 104', now, now),
        (5, 5, 'Friday', '11:00 AM', 'Room 105', now, now)
    ]
    cursor.executemany("INSERT INTO course_schedule (id, course_id, day, time, room, created_at, updated_at) VALUES (?, ?, ?, ?, ?, ?, ?);", course_schedule)


    conn.commit()
    conn.close()

if __name__ == "__main__":
    populate_db()
