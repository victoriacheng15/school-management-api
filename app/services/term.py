from app.models import (
    term_db_read_all,
    term_db_read_by_id,
    term_db_read_by_ids,
    term_db_insert,
    term_db_update,
)
from app.utils import (
    term_row_to_dict,
    term_dict_to_row,
    bulk_create_entities,
    bulk_update_entities,
)


def get_all_terms():
    results = term_db_read_all()
    if results is None:
        raise RuntimeError("Failed to fetch terms.")
    return [term_row_to_dict(term) for term in results]


def get_term_by_id(term_id: int):
    term = term_db_read_by_id(term_id)
    return term_row_to_dict(term) if term else None


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
