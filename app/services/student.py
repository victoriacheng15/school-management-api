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
    created_ids = []
    errors = []

    for student_data in students:
        student_data = {
            k: (v.strip() if isinstance(v, str) else v) for k, v in student_data.items()
        }

        try:
            row = student_dict_to_row(student_data)
            student_id = create_student(row)
            if student_id:
                created_ids.append(student_id)
            else:
                errors.append(
                    {
                        "student": student_data,
                        "error": "Failed to insert student (unknown DB error)",
                    }
                )
        except (ValueError, RuntimeError) as e:
            errors.append({"student": student_data, "error": str(e)})

    if not created_ids:
        return [], {"error": "No students were created", "details": errors}, 400

    created_students_rows = read_students_by_ids(created_ids)
    created_students = [student_row_to_dict(row) for row in created_students_rows]

    if errors:
        return {"created": created_students, "errors": errors}, None, 201

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
            errors.append(
                {"student": incoming_data, "error": "Missing student ID for update"}
            )
            continue

        existing_data = get_student_by_id(student_id)
        if not existing_data:
            errors.append(
                {
                    "student": incoming_data,
                    "error": f"Student ID {student_id} not found",
                }
            )
            continue

        # Merge the incoming fields into the full existing object
        full_data = {**existing_data, **incoming_data}

        try:
            row = student_dict_to_row(full_data)
            success = update_student(student_id, row)
            if success:
                updated_ids.append(student_id)
            else:
                errors.append(
                    {
                        "student": incoming_data,
                        "error": f"Student ID {student_id} not updated (maybe archived?)",
                    }
                )
        except (ValueError, RuntimeError) as e:
            errors.append({"student": incoming_data, "error": str(e)})

    if not updated_ids:
        return [], {"error": "No students were updated", "details": errors}, 400

    updated_students_rows = read_students_by_ids(updated_ids)
    updated_students = [student_row_to_dict(row) for row in updated_students_rows]

    if errors:
        return {"updated": updated_students, "errors": errors}, None, 200

    return updated_students, None, 200


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
