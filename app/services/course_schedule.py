from app.models import (
    course_schedule_db_read_all,
    course_schedule_db_read_by_id,
    course_schedule_db_read_by_ids,
    course_schedule_db_insert,
    course_schedule_db_update,
    course_schedule_db_archive,
)
from app.utils import (
    course_schedule_dict_to_row,
    bulk_create_entities,
    bulk_update_entities,
    bulk_archive_entities,
)


def course_schedule_row_to_dict(row):
    return row if isinstance(row, dict) else row


def get_all_course_schedules(active_only):
    results = course_schedule_db_read_all(active_only=active_only)
    if results is None:
        raise RuntimeError("Failed to fetch course schedules.")
    return results  # Already dicts from model


def get_course_schedule_by_id(course_schedule_id: int):
    course_schedule = course_schedule_db_read_by_id(course_schedule_id)
    return course_schedule  # Already dict from model


def create_new_course_schedules(data):
    return bulk_create_entities(
        data,
        insert_func=course_schedule_db_insert,
        to_row_func=course_schedule_dict_to_row,
        to_dict_func=course_schedule_row_to_dict,
        read_by_ids_func=course_schedule_db_read_by_ids,
        no_success_msg="No course schedules were created.",
        success_status_code=201,
        failure_status_code=400,
    )


def update_course_schedules(data):
    return bulk_update_entities(
        data,
        update_func=course_schedule_db_update,
        get_existing_func=course_schedule_db_read_by_id,
        to_row_func=course_schedule_dict_to_row,
        to_dict_func=course_schedule_row_to_dict,
        read_by_ids_func=course_schedule_db_read_by_ids,
        no_success_msg="No course schedules were updated.",
        missing_id_msg="Missing course schedule ID for update.",
        not_found_msg="Course schedule ID {id} not found.",
        not_updated_msg="Course schedule ID {id} not updated.",
        failure_status_code=400,
        success_status_code=200,
    )


def archive_course_schedules(ids):
    return bulk_archive_entities(
        ids,
        archive_func=course_schedule_db_archive,
        get_existing_func=course_schedule_db_read_by_id,
        to_dict_func=course_schedule_row_to_dict,
        read_by_ids_func=course_schedule_db_read_by_ids,
        no_success_msg="No course schedules were archived.",
        not_found_msg="Course schedule ID {id} not found or already archived.",
        not_updated_msg="Course schedule ID {id} not archived.",
        failure_status_code=422,
        success_status_code=200,
    )
