from app.models import (
    course_db_read_all,
    course_db_read_by_id,
    course_db_read_by_ids,
    course_db_insert,
    course_db_update,
    course_db_archive,
)
from app.utils import (
    course_dict_to_row,
    bulk_create_entities,
    bulk_update_entities,
    bulk_archive_entities,
)


def course_row_to_dict(row):
    return row if isinstance(row, dict) else row


def get_all_courses(active_only):
    results = course_db_read_all(active_only=active_only)
    if results is None:
        raise RuntimeError("Failed to fetch courses.")
    return results


def get_course_by_id(course_id: int):
    course = course_db_read_by_id(course_id)
    return course


def create_new_courses(data):
    return bulk_create_entities(
        data,
        insert_func=course_db_insert,
        to_row_func=course_dict_to_row,
        to_dict_func=course_row_to_dict,
        read_by_ids_func=course_db_read_by_ids,
        no_success_msg="No courses were created.",
        success_status_code=201,
        failure_status_code=400,
    )


def update_courses(data):
    return bulk_update_entities(
        data,
        update_func=course_db_update,
        get_existing_func=course_db_read_by_id,
        to_row_func=course_dict_to_row,
        to_dict_func=course_row_to_dict,
        read_by_ids_func=course_db_read_by_ids,
        no_success_msg="No courses were updated.",
        missing_id_msg="Missing course ID for update.",
        not_found_msg="Course ID {id} not found.",
        not_updated_msg="Course ID {id} not updated.",
        failure_status_code=400,
        success_status_code=200,
    )


def archive_courses(ids):
    return bulk_archive_entities(
        ids,
        archive_func=course_db_archive,
        get_existing_func=course_db_read_by_id,
        to_dict_func=course_row_to_dict,
        read_by_ids_func=course_db_read_by_ids,
        no_success_msg="No courses were archived.",
        not_found_msg="Course ID {id} not found or already archived.",
        not_updated_msg="Course ID {id} not archived.",
        failure_status_code=422,
        success_status_code=200,
    )
