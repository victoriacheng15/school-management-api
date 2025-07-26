from app.models import (
    department_db_read_all,
    department_db_read_by_id,
    department_db_read_by_ids,
    department_db_insert,
    department_db_update,
    department_db_archive,
)
from app.utils import (
    department_row_to_dict,
    department_dict_to_row,
    normalize_to_list,
)


def get_all_departments(active_only):
    results = department_db_read_all(active_only=active_only)
    if results is None:
        raise RuntimeError("Failed to fetch departments.")
    return [department_row_to_dict(department) for department in results]


def get_department_by_id(department_id: int):
    department = department_db_read_by_id(department_id)
    if department is None:
        return None
    return department_row_to_dict(department)


def create_new_departments(data):
    departments = normalize_to_list(data)
    created_ids = []
    errors = []

    for department_data in departments:
        department_data = {
            k: (v.strip() if isinstance(v, str) else v)
            for k, v in department_data.items()
        }

        try:
            row = department_dict_to_row(department_data)
            department_id = department_db_insert(row)
            if department_id:
                created_ids.append(department_id)
            else:
                errors.append(
                    {"message": "Failed to insert department (unknown DB error)."}
                )
        except (ValueError, RuntimeError) as e:
            errors.append({"message": str(e)})

    if not created_ids:
        return [], {"message": "No departments were created.", "details": errors}, 400

    created_departments_rows = department_db_read_by_ids(created_ids)
    created_departments = [
        department_row_to_dict(row) for row in created_departments_rows
    ]

    return created_departments, None, 201


def update_departments(data):
    departments = normalize_to_list(data)
    updated_ids = []
    errors = []

    for incoming_data in departments:
        incoming_data = {
            k: (v.strip() if isinstance(v, str) else v)
            for k, v in incoming_data.items()
        }

        department_id = incoming_data.get("id")
        if not department_id:
            return [], [{"message": "Missing department ID for update."}], 400

        existing_data = department_db_read_by_id(department_id)
        if not existing_data:
            return [], [{"message": f"Department ID {department_id} not found."}], 404

        if not isinstance(existing_data, dict):
            existing_data = department_row_to_dict(existing_data)

        full_data = {**existing_data, **incoming_data}

        try:
            row = department_dict_to_row(full_data)
            success = department_db_update(department_id, row)
            if success:
                updated_ids.append(department_id)
            else:
                errors.append(
                    {"message": f"Department ID {department_id} not updated."}
                )
        except (ValueError, RuntimeError) as e:
            errors.append({"message": str(e)})

    if not updated_ids:
        return [], errors, 400

    updated_departments_rows = department_db_read_by_ids(updated_ids)
    updated_departments = [
        department_row_to_dict(row) for row in updated_departments_rows
    ]

    return updated_departments, errors, 200


def archive_departments(ids):
    ids = normalize_to_list(ids)
    if not all(isinstance(item, int) for item in ids):
        return [], [{"message": "IDs must be integers"}], 400

    archived_ids = []
    errors = []

    for department_id in ids:
        rows_updated = department_db_archive(department_id)
        if rows_updated > 0:
            archived_ids.append(department_id)
        else:
            errors.append(
                {
                    "message": f"Department ID {department_id} is not found or already archived)"
                }
            )

    if not archived_ids:
        return [], errors, 42

    archived_rows = department_db_read_by_ids(archived_ids)
    archived_departments = [department_row_to_dict(row) for row in archived_rows]

    return archived_departments, errors, 200
