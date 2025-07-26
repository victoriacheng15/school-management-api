from app.models import (
    instructor_db_read_all,
    instructor_db_read_by_id,
    instructor_db_read_by_ids,
    instructor_db_insert,
    instructor_db_update,
    instructor_db_archive,
)
from app.utils import (
    instructor_row_to_dict,
    instructor_dict_to_row,
    normalize_to_list,
)


def get_all_instructors(active_only):
    results = instructor_db_read_all(active_only=active_only)
    if results is None:
        raise RuntimeError("Failed to fetch instructors.")
    return [instructor_row_to_dict(instructor) for instructor in results]


def get_instructor_by_id(instructor_id: int):
    instructor = instructor_db_read_by_id(instructor_id)
    if instructor is None:
        return None
    return instructor_row_to_dict(instructor)


def create_new_instructors(data):
    instructors = normalize_to_list(data)
    created_ids = []
    errors = []

    for instructor_data in instructors:
        instructor_data = {
            k: (v.strip() if isinstance(v, str) else v)
            for k, v in instructor_data.items()
        }

        try:
            row = instructor_dict_to_row(instructor_data)
            instructor_id = instructor_db_insert(row)
            if instructor_id:
                created_ids.append(instructor_id)
            else:
                errors.append({"message": "Failed to insert instructor (unknown DB error)."})
        except (ValueError, RuntimeError) as e:
            errors.append({"message": str(e)})

    if not created_ids:
        return [], {"message": "No instructors were created", "details": errors}, 400

    created_instructors_rows = instructor_db_read_by_ids(created_ids)
    created_instructors = [
        instructor_row_to_dict(row) for row in created_instructors_rows
    ]

    return created_instructors, None, 201


def update_instructors(data):
    instructors = normalize_to_list(data)
    updated_ids = []
    errors = []

    for incoming_data in instructors:
        incoming_data = {
            k: (v.strip() if isinstance(v, str) else v)
            for k, v in incoming_data.items()
        }

        instructor_id = incoming_data.get("id")
        if not instructor_id:
            return [], [{"message": "Missing instructor ID for update."}], 400

        existing_data = instructor_db_read_by_id(instructor_id)
        if not existing_data:
            return [], [{"message": f"Instructor ID {instructor_id} not found."}], 422
        
        if not isinstance(existing_data, dict):
            existing_data = instructor_row_to_dict(existing_data)

        full_data = {**existing_data, **incoming_data}

        try:
            row = instructor_dict_to_row(full_data)
            success = instructor_db_update(instructor_id, row)
            if success:
                updated_ids.append(instructor_id)
            else:
                errors.append(
                    {
                        "message": f"Instructor ID {instructor_id} not updated.",
                    }
                )
        except (ValueError, RuntimeError) as e:
            errors.append({"message": str(e)})

    if not updated_ids:
        return [], errors, 400

    updated_instructors_rows = instructor_db_read_by_ids(updated_ids)
    updated_instructors = [
        instructor_row_to_dict(row) for row in updated_instructors_rows
    ]

    return updated_instructors, errors, 200


def archive_instructors(ids):
    ids = normalize_to_list(ids)
    if not all(isinstance(item, int) for item in ids):
        return [], [{"message": "IDs must be integers"}], 400

    archived_ids = []
    errors = []

    for instructor_id in ids:
        rows_updated = instructor_db_archive(instructor_id)
        if rows_updated > 0:
            archived_ids.append(instructor_id)
        else:
            errors.append({"message": f"Instructor ID {instructor_id} is not found or already archived.",})

    if not archived_ids:
        return [], errors, 422

    archived_rows = instructor_db_read_by_ids(archived_ids)
    archived_instructors = [instructor_row_to_dict(row) for row in archived_rows]

    return archived_instructors, errors, 200
