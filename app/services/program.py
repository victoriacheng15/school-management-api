from app.models import (
    program_db_read_all,
    program_db_read_by_id,
    program_db_read_by_ids,
    program_db_insert,
    program_db_update,
    program_db_archive,
)
from app.utils import (
    program_dict_to_row,
    bulk_create_entities,
    bulk_update_entities,
    bulk_archive_entities,
)


def program_row_to_dict(row):
    return row if isinstance(row, dict) else row


def get_all_programs(active_only):
    results = program_db_read_all(active_only=active_only)
    if results is None:
        raise RuntimeError("Failed to fetch programs.")
    return results


def get_program_by_id(program_id: int):
    program = program_db_read_by_id(program_id)
    return program  # already dict from model


def create_new_programs(data):
    return bulk_create_entities(
        data,
        insert_func=program_db_insert,
        to_row_func=program_dict_to_row,
    to_dict_func=program_row_to_dict,
        read_by_ids_func=program_db_read_by_ids,
        no_success_msg="No programs were created.",
        success_status_code=201,
        failure_status_code=400,
    )


def update_programs(data):
    return bulk_update_entities(
        data,
        update_func=program_db_update,
        get_existing_func=program_db_read_by_id,
        to_row_func=program_dict_to_row,
    to_dict_func=program_row_to_dict,
        read_by_ids_func=program_db_read_by_ids,
        no_success_msg="No programs were updated.",
        missing_id_msg="Missing program ID for update.",
        not_found_msg="Program ID {id} not found.",
        not_updated_msg="Program ID {id} not updated.",
        failure_status_code=400,
        success_status_code=200,
    )


def archive_programs(ids):
    return bulk_archive_entities(
        ids,
        archive_func=program_db_archive,
        get_existing_func=program_db_read_by_id,
    to_dict_func=program_row_to_dict,
        read_by_ids_func=program_db_read_by_ids,
        no_success_msg="No programs were archived.",
        not_found_msg="Program ID {id} not found or already archived.",
        not_updated_msg="Program ID {id} not archived.",
        failure_status_code=422,
        success_status_code=200,
    )
