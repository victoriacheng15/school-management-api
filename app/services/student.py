from app.models import (
    student_db_read_all,
    student_db_read_by_id,
    student_db_read_by_ids,
    student_db_insert,
    student_db_update,
    student_db_archive,
)
from app.utils import (
    student_row_to_dict,
    student_dict_to_row,
    bulk_create_entities,
    bulk_update_entities,
    bulk_archive_entities,
)


def get_all_students(active_only):
    results = student_db_read_all(active_only=active_only)
    if results is None:
        raise RuntimeError("Failed to fetch students.")
    return [student_row_to_dict(student) for student in results]


def get_student_by_id(student_id: int):
    student = student_db_read_by_id(student_id)
    return student_row_to_dict(student) if student else None


def create_new_students(data):
    return bulk_create_entities(
        data,
        insert_func=student_db_insert,
        to_row_func=student_dict_to_row,
        to_dict_func=student_row_to_dict,
        read_by_ids_func=student_db_read_by_ids,
        no_success_msg="No students were created.",
        success_status_code=201,
        failure_status_code=400,
    )


def update_students(data):
    return bulk_update_entities(
        data,
        update_func=student_db_update,
        get_existing_func=student_db_read_by_id,
        to_row_func=student_dict_to_row,
        to_dict_func=student_row_to_dict,
        read_by_ids_func=student_db_read_by_ids,
        no_success_msg="No students were updated.",
        missing_id_msg="Missing student ID for update.",
        not_found_msg="Student ID {id} not found.",
        not_updated_msg="Student ID {id} not updated.",
        failure_status_code=400,
        success_status_code=200,
    )

def archive_students(ids):
    return bulk_archive_entities(
        ids,
        archive_func=student_db_archive,
        get_existing_func=student_db_read_by_id,
        to_dict_func=student_row_to_dict,
        read_by_ids_func=student_db_read_by_ids,
        no_success_msg="No students were archived.",
        not_found_msg="Student ID {id} not found or already archived.",
        not_updated_msg="Student ID {id} not archived.",
        failure_status_code=422,
        success_status_code=200,
    )
