from app.models import (
    program_db_read_all,
    program_db_read_by_id,
    program_db_read_by_ids,
    program_db_insert,
    program_db_update,
    program_db_archive,
)
from app.utils.converters import (
    program_row_to_dict,
    program_dict_to_row,
)
from app.utils.routes_helpers import (
    normalize_to_list,
)


def get_all_programs(active_only):
    results = program_db_read_all(active_only=active_only)
    if results is None:
        raise RuntimeError("Failed to fetch programs.")
    return [program_row_to_dict(program) for program in results]


def get_program_by_id(program_id: int):
    program = program_db_read_by_id(program_id)
    if program is None:
        return None
    return program_row_to_dict(program)


def create_new_programs(data):
    programs = normalize_to_list(data)
    created_ids = []
    errors = []

    for program_data in programs:
        program_data = {
            k: (v.strip() if isinstance(v, str) else v) for k, v in program_data.items()
        }

        try:
            row = program_dict_to_row(program_data)
            program_id = program_db_insert(row)
            if program_id:
                created_ids.append(program_id)
            else:
                errors.append(
                    {"message": "Failed to insert program (unknown DB error)."}
                )
        except (ValueError, RuntimeError) as e:
            errors.append({"message": str(e)})

    if not created_ids:
        return [], {"message": "No programs were created", "details": errors}, 400

    created_programs_rows = program_db_read_by_ids(created_ids)
    created_programs = [program_row_to_dict(row) for row in created_programs_rows]

    return created_programs, None, 201


def update_programs(data):
    programs = normalize_to_list(data)
    updated_ids = []
    errors = []

    for incoming_data in programs:
        incoming_data = {
            k: (v.strip() if isinstance(v, str) else v)
            for k, v in incoming_data.items()
        }

        program_id = incoming_data.get("id")
        if not program_id:
            return [], [{"message": "Missing program ID for update."}], 400

        existing_data = program_db_read_by_id(program_id)
        if not existing_data:
            return [], [{"message": f"Program ID {program_id} not found."}], 422

        if not isinstance(existing_data, dict):
            existing_data = program_row_to_dict(existing_data)

        full_data = {**existing_data, **incoming_data}

        try:
            row = program_dict_to_row(full_data)
            success = program_db_update(program_id, row)
            if success:
                updated_ids.append(program_id)
            else:
                errors.append({"message": f"Program ID {program_id} not updated."})
        except (ValueError, RuntimeError) as e:
            errors.append({"message": str(e)})

    if not updated_ids:
        return [], errors, 400

    updated_programs_rows = program_db_read_by_ids(updated_ids)
    updated_programs = [program_row_to_dict(row) for row in updated_programs_rows]

    return updated_programs, errors, 200


def archive_programs(ids):
    ids = normalize_to_list(ids)
    if not all(isinstance(item, int) for item in ids):
        return [], [{"message": "IDs must be integers"}], 400

    archived_ids = []
    errors = []

    for program_id in ids:
        rows_updated = program_db_archive(program_id)
        if rows_updated > 0:
            archived_ids.append(program_id)
        else:
            errors.append(
                {"message": f"Program ID {program_id} not found or already archived."}
            )

    if not archived_ids:
        return [], errors, 422

    # Read and return the updated records
    archived_rows = program_db_read_by_ids(archived_ids)
    archived_programs = [program_row_to_dict(row) for row in archived_rows]

    return archived_programs, errors, 200