from app.models import (
    term_db_read_all,
    term_db_read_by_id,
    term_db_read_by_ids,
    term_db_insert,
    term_db_update,
    term_db_archive,
)
from app.utils import (
    term_row_to_dict,
    term_dict_to_row,
    bulk_create_entities,
    bulk_update_entities,
    bulk_archive_entities,
)


def term_row_to_dict(row):
    return row if isinstance(row, dict) else row


def get_all_terms(active_only):
    results = term_db_read_all(active_only=active_only)
    if results is None:
        raise RuntimeError("Failed to fetch terms.")
    return results  # Already dicts from model


def get_term_by_id(term_id: int):
    term = term_db_read_by_id(term_id)
    return term  # Already dict from model


def create_new_terms(data):
    return bulk_create_entities(
        data,
        insert_func=term_db_insert,
        to_row_func=term_dict_to_row,
        to_dict_func=term_row_to_dict,
        read_by_ids_func=term_db_read_by_ids,
        no_success_msg="No terms were created.",
        success_status_code=201,
        failure_status_code=400,
    )


def update_terms(data):
    return bulk_update_entities(
        data,
        update_func=term_db_update,
        get_existing_func=term_db_read_by_id,
        to_row_func=term_dict_to_row,
        to_dict_func=term_row_to_dict,
        read_by_ids_func=term_db_read_by_ids,
        no_success_msg="No terms were updated.",
        missing_id_msg="Missing term ID for update.",
        not_found_msg="Term ID {id} not found.",
        not_updated_msg="Term ID {id} not updated.",
        failure_status_code=400,
        success_status_code=200,
    )


def archive_terms(ids):
    return bulk_archive_entities(
        ids,
        archive_func=term_db_archive,
        get_existing_func=term_db_read_by_id,
        to_dict_func=term_row_to_dict,
        read_by_ids_func=term_db_read_by_ids,
        no_success_msg="No terms were archived.",
        not_found_msg="Term ID {id} not found or already archived.",
        not_updated_msg="Term ID {id} not archived.",
        failure_status_code=422,
        success_status_code=200,
    )
