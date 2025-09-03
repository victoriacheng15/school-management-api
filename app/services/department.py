from app.models import (
    department_db_read_all,
    department_db_read_by_id,
    department_db_read_by_ids,
    department_db_insert,
    department_db_update,
    department_db_archive,
)
from app.utils import (
    department_dict_to_row,
    bulk_create_entities,
    bulk_update_entities,
    bulk_archive_entities,
)


def department_row_to_dict(row):
    return row if isinstance(row, dict) else row

def get_all_departments(active_only):
    results = department_db_read_all(active_only=active_only)
    if results is None:
        raise RuntimeError("Failed to fetch departments.")
    return results  # already dicts from model


def get_department_by_id(department_id: int):
    department = department_db_read_by_id(department_id)
    return department  # already dict from model


def create_new_departments(data):
    return bulk_create_entities(
        data,
        insert_func=department_db_insert,
        to_row_func=department_dict_to_row,
        to_dict_func=department_row_to_dict,
        read_by_ids_func=department_db_read_by_ids,
        no_success_msg="No departments were created.",
        success_status_code=201,
        failure_status_code=400,
    )


def update_departments(data):
    return bulk_update_entities(
        data,
        update_func=department_db_update,
        get_existing_func=department_db_read_by_id,
        to_row_func=department_dict_to_row,
        to_dict_func=department_row_to_dict,
        read_by_ids_func=department_db_read_by_ids,
        no_success_msg="No departments were updated.",
        missing_id_msg="Missing department ID for update.",
        not_found_msg="Department ID {id} not found.",
        not_updated_msg="Department ID {id} not updated.",
        failure_status_code=400,
        success_status_code=200,
    )


def archive_departments(ids):
    return bulk_archive_entities(
        ids,
        archive_func=department_db_archive,
        get_existing_func=department_db_read_by_id,
        to_dict_func=department_row_to_dict,
        read_by_ids_func=department_db_read_by_ids,
        no_success_msg="No departments were archived.",
        not_found_msg="Department ID {id} not found or already archived.",
        not_updated_msg="Department ID {id} not archived.",
        failure_status_code=422,
        success_status_code=200,
    )
