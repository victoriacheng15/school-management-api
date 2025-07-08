from app.models import (
    read_all_active_students,
    create_student,
    read_student_by_id,
    update_student,
    archive_student,
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
    results, error = handle_bulk_process(
        items=students,
        process_func=create_student,
        success_func=read_student_by_id,
        dict_to_row_func=student_dict_to_row,
        row_to_dict_func=student_row_to_dict
    )
    return results, error


def update_students(data):
    students = normalize_to_list(data)
    results, error = handle_bulk_process(
        items=students,
        process_func=update_student,
        success_func=read_student_by_id,
        id_key="id",
        missing_id_msg="Missing 'id' field in student update data",
        dict_to_row_func=student_dict_to_row,
        row_to_dict_func=student_row_to_dict
    )
    return results, error


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
