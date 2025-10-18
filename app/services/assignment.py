from app.models import (
    assignment_db_read_all,
    assignment_db_read_by_id,
    assignment_db_read_by_ids,
    assignment_db_insert,
    assignment_db_update,
    assignment_db_archive,
)
from app.utils import (
    assignment_dict_to_row,
    bulk_create_entities,
    bulk_update_entities,
    bulk_archive_entities,
)


def assignment_row_to_dict(row):
    return row if isinstance(row, dict) else row


def get_all_assignments(active_only):
    results = assignment_db_read_all(active_only=active_only)
    if results is None:
        raise RuntimeError("Failed to fetch assignments.")
    return results


def get_assignment_by_id(assignment_id: int):
    assignment = assignment_db_read_by_id(assignment_id)
    return assignment


def create_new_assignments(data):
    return bulk_create_entities(
        data,
        insert_func=assignment_db_insert,
        to_row_func=assignment_dict_to_row,
        to_dict_func=assignment_row_to_dict,
        read_by_ids_func=assignment_db_read_by_ids,
        no_success_msg="No assignments were created.",
        success_status_code=201,
        failure_status_code=400,
    )


def update_assignments(data):
    return bulk_update_entities(
        data,
        update_func=assignment_db_update,
        get_existing_func=assignment_db_read_by_id,
        to_row_func=assignment_dict_to_row,
        to_dict_func=assignment_row_to_dict,
        read_by_ids_func=assignment_db_read_by_ids,
        no_success_msg="No assignments were updated.",
        missing_id_msg="Missing assignment ID for update.",
        not_found_msg="Assignment ID {id} not found.",
        not_updated_msg="Assignment ID {id} not updated.",
        failure_status_code=400,
        success_status_code=200,
    )


def archive_assignments(ids):
    return bulk_archive_entities(
        ids,
        archive_func=assignment_db_archive,
        get_existing_func=assignment_db_read_by_id,
        to_dict_func=assignment_row_to_dict,
        read_by_ids_func=assignment_db_read_by_ids,
        no_success_msg="No assignments were archived.",
        not_found_msg="Assignment ID {id} not found or already archived.",
        not_updated_msg="Assignment ID {id} not archived.",
        failure_status_code=422,
        success_status_code=200,
    )
