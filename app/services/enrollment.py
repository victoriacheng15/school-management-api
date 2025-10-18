from app.models import (
    enrollment_db_read_all,
    enrollment_db_read_by_id,
    enrollment_db_read_by_ids,
    enrollment_db_insert,
    enrollment_db_update,
    enrollment_db_archive,
)
from app.utils import (
    enrollment_dict_to_row,
    bulk_create_entities,
    bulk_update_entities,
    bulk_archive_entities,
)


def enrollment_row_to_dict(row):
    return row if isinstance(row, dict) else row


def get_all_enrollments(active_only):
    results = enrollment_db_read_all(active_only=active_only)
    if results is None:
        raise RuntimeError("Failed to fetch enrollments.")
    return results


def get_enrollment_by_id(enrollment_id: int):
    enrollment = enrollment_db_read_by_id(enrollment_id)
    return enrollment


def create_new_enrollments(data):
    return bulk_create_entities(
        data,
        insert_func=enrollment_db_insert,
        to_row_func=enrollment_dict_to_row,
        to_dict_func=enrollment_row_to_dict,
        read_by_ids_func=enrollment_db_read_by_ids,
        no_success_msg="No enrollments were created.",
        success_status_code=201,
        failure_status_code=400,
    )


def update_enrollments(data):
    return bulk_update_entities(
        data,
        update_func=enrollment_db_update,
        get_existing_func=enrollment_db_read_by_id,
        to_row_func=enrollment_dict_to_row,
        to_dict_func=enrollment_row_to_dict,
        read_by_ids_func=enrollment_db_read_by_ids,
        no_success_msg="No enrollments were updated.",
        missing_id_msg="Missing enrollment ID for update.",
        not_found_msg="Enrollment ID {id} not found.",
        not_updated_msg="Enrollment ID {id} not updated.",
        failure_status_code=400,
        success_status_code=200,
    )


def archive_enrollments(ids):
    return bulk_archive_entities(
        ids,
        archive_func=enrollment_db_archive,
        get_existing_func=enrollment_db_read_by_id,
        to_dict_func=enrollment_row_to_dict,
        read_by_ids_func=enrollment_db_read_by_ids,
        no_success_msg="No enrollments were archived.",
        not_found_msg="Enrollment ID {id} not found or already archived.",
        not_updated_msg="Enrollment ID {id} not archived.",
        failure_status_code=422,
        success_status_code=200,
    )
