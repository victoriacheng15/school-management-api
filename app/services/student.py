from app.models import (
    read_all_active_students,
    create_student,
    read_student_by_id,
    update_student,
    archive_student,
    read_students_by_ids,
)
from app.utils import (
    student_row_to_dict,
    student_dict_to_row,
    handle_bulk_process,
    normalize_to_list,
)


def get_all_active_students():
    results = read_all_active_students()
    if results is None:
        raise RuntimeError("Failed to fetch students")
    return [student_row_to_dict(student) for student in results]


def get_student_by_id(student_id: int):
    student = read_student_by_id(student_id)
    if student is None:
        return None
    return student_row_to_dict(student)


def create_students(data):
    students = normalize_to_list(data)

    # Bulk create students
    created_ids = []
    for student_data in students:
        row = student_dict_to_row(student_data)
        student_id = create_student(row)
        if student_id:
            created_ids.append(student_id)

    if not created_ids:
        return [], None

    # Fetch all created students in a single query
    created_students_rows = read_students_by_ids(created_ids)
    return [student_row_to_dict(row) for row in created_students_rows], None


def update_students(data):
    students = normalize_to_list(data)

    updated_ids = []
    for student_data in students:
        student_id = student_data.get("id")
        if not student_id:
            continue
        row = student_dict_to_row(student_data)
        if update_student(student_id, row):
            updated_ids.append(student_id)

    if not updated_ids:
        return [], None

    updated_students_rows = read_students_by_ids(updated_ids)
    return [student_row_to_dict(row) for row in updated_students_rows], None


def archive_students(ids):
    ids = normalize_to_list(ids)
    if not all(isinstance(item, int) for item in ids):
        raise ValueError("IDs must be integers")

    archived_ids = []
    for student_id in ids:
        rows_updated = archive_student(student_id)
        if rows_updated > 0:
            archived_ids.append(student_id)

    return archived_ids
