from app.models import (
    instructor_db_read_all,
    instructor_db_read_by_id,
    instructor_db_read_by_ids,
    instructor_db_insert,
    instructor_db_update,
    instructor_db_archive,
)
from app.utils import (
    instructor_dict_to_row,
    bulk_create_entities,
    bulk_update_entities,
    bulk_archive_entities,
)


def instructor_row_to_dict(row):
    return row if isinstance(row, dict) else row


def get_all_instructors(active_only):
    results = instructor_db_read_all(active_only=active_only)
    if results is None:
        raise RuntimeError("Failed to fetch instructors.")
    return results  # Already dicts from model


def get_instructor_by_id(instructor_id: int):
    instructor = instructor_db_read_by_id(instructor_id)
    return instructor  # Already dict from model


def create_new_instructors(data):
    return bulk_create_entities(
        data,
        insert_func=instructor_db_insert,
        to_row_func=instructor_dict_to_row,
        to_dict_func=instructor_row_to_dict,
        read_by_ids_func=instructor_db_read_by_ids,
        no_success_msg="No instructors were created.",
        success_status_code=201,
        failure_status_code=400,
    )


def update_instructors(data):
    return bulk_update_entities(
        data,
        update_func=instructor_db_update,
        get_existing_func=instructor_db_read_by_id,
        to_row_func=instructor_dict_to_row,
        to_dict_func=instructor_row_to_dict,
        read_by_ids_func=instructor_db_read_by_ids,
        no_success_msg="No instructors were updated.",
        missing_id_msg="Missing instructor ID for update.",
        not_found_msg="Instructor ID {id} not found.",
        not_updated_msg="Instructor ID {id} not updated.",
        failure_status_code=400,
        success_status_code=200,
    )


def archive_instructors(ids):
    return bulk_archive_entities(
        ids,
        archive_func=instructor_db_archive,
        get_existing_func=instructor_db_read_by_id,
        to_dict_func=instructor_row_to_dict,
        read_by_ids_func=instructor_db_read_by_ids,
        no_success_msg="No instructors were archived.",
        not_found_msg="Instructor ID {id} not found or already archived.",
        not_updated_msg="Instructor ID {id} not archived.",
        failure_status_code=422,
        success_status_code=200,
    )
