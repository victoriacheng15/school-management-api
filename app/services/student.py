from app.models import (
    student_db_read_all,
    student_db_read_by_id,
    student_db_read_by_ids,
    student_db_insert,
    student_db_update,
    student_db_archive,
)
from app.utils import (
    student_row_to_dict,
    student_dict_to_row,
    normalize_to_list,
)


def get_all_students(active_only):
    results = student_db_read_all(active_only=active_only)
    if results is None:
        raise RuntimeError("Failed to fetch students")
    return [student_row_to_dict(student) for student in results]


def get_student_by_id(student_id: int):
    student = student_db_read_by_id(student_id)
    if student is None:
        return None
    return student_row_to_dict(student)


def create_new_students(data):
    students = normalize_to_list(data)
    created_ids = []
    errors = []

    for student_data in students:
        student_data = {
            k: (v.strip() if isinstance(v, str) else v) for k, v in student_data.items()
        }

        try:
            row = student_dict_to_row(student_data)
            student_id = student_db_insert(row)
            if student_id:
                created_ids.append(student_id)
            else:
                errors.append(
                    {
                        "message": "Failed to insert student (unknown DB error)",
                    }
                )
        except (ValueError, RuntimeError) as e:
            errors.append({"message": str(e)})

    if not created_ids:
        return [], {"message": "No students were created", "details": errors}, 400

    created_students_rows = student_db_read_by_ids(created_ids)
    created_students = [student_row_to_dict(row) for row in created_students_rows]

    return created_students, None, 201


def update_students(data):
    students = normalize_to_list(data)
    updated_ids = []
    errors = []

    for incoming_data in students:
        incoming_data = {
            k: (v.strip() if isinstance(v, str) else v)
            for k, v in incoming_data.items()
        }

        student_id = incoming_data.get("id")
        if not student_id:
            errors.append({"message": "Missing student ID for update"})
            continue

        existing_data = student_db_read_by_id(student_id)
        if not existing_data:
            errors.append(
                {
                    "message": f"Student ID {student_id} not found",
                }
            )
            continue
        if not isinstance(existing_data, dict):
            existing_data = student_row_to_dict(existing_data)

        full_data = {**existing_data, **incoming_data}

        try:
            row = student_dict_to_row(full_data)
            success = student_db_update(student_id, row)
            if success:
                updated_ids.append(student_id)
            else:
                errors.append(
                    {
                        "message": f"Student ID {student_id} not updated (maybe archived?)",
                    }
                )
        except (ValueError, RuntimeError) as e:
            errors.append({"message": str(e)})

    if not updated_ids:
        return [], errors, 400

    updated_students_rows = student_db_read_by_ids(updated_ids)
    updated_students = [student_row_to_dict(row) for row in updated_students_rows]

    return updated_students, errors, 200


def archive_students(ids):
    ids = normalize_to_list(ids)
    if not all(isinstance(item, int) for item in ids):
        raise ValueError("IDs must be integers")

    archived_ids = []
    errors = []

    for student_id in ids:
        rows_updated = student_db_archive(student_id)
        if rows_updated > 0:
            archived_ids.append(student_id)
        else:
            errors.append(
                {
                    "id": student_id,
                    "message": f"Student ID {student_id} is not found or already archived)",
                }
            )

    if not archived_ids:
        return [], errors, 400

    # Read and return the updated records
    archived_rows = student_db_read_by_ids(archived_ids)
    archived_students = [student_row_to_dict(row) for row in archived_rows]

    return archived_students, errors, 200
