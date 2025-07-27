from app.models import (
    course_db_read_all,
    course_db_read_by_id,
    course_db_read_by_ids,
    course_db_insert,
    course_db_update,
    course_db_archive,
)
from app.utils.converters import (
    course_row_to_dict,
    course_dict_to_row,
)
from app.utils.routes_helpers import (
    normalize_to_list,
)


def get_all_courses(active_only):
    results = course_db_read_all(active_only=active_only)
    if results is None:
        raise RuntimeError("Failed to fetch courses.")
    return [course_row_to_dict(course) for course in results]


def get_course_by_id(course_id: int):
    course = course_db_read_by_id(course_id)
    if course is None:
        return None
    return course_row_to_dict(course)


def create_new_courses(data):
    courses = normalize_to_list(data)
    created_ids = []
    errors = []

    for course_data in courses:
        course_data = {
            k: (v.strip() if isinstance(v, str) else v) for k, v in course_data.items()
        }

        try:
            row = course_dict_to_row(course_data)
            course_id = course_db_insert(row)
            if course_id:
                created_ids.append(course_id)
            else:
                errors.append(
                    {"message": "Failed to insert course (unknown DB error)."}
                )
        except (ValueError, RuntimeError) as e:
            errors.append({"message": str(e)})

    if not created_ids:
        return [], {"message": "No courses were created", "details": errors}, 400

    created_courses_rows = course_db_read_by_ids(created_ids)
    created_courses = [course_row_to_dict(row) for row in created_courses_rows]

    return created_courses, None, 201


def update_courses(data):
    courses = normalize_to_list(data)
    updated_ids = []
    errors = []

    for incoming_data in courses:
        incoming_data = {
            k: (v.strip() if isinstance(v, str) else v)
            for k, v in incoming_data.items()
        }

        course_id = incoming_data.get("id")
        if not course_id:
            return [], [{"message": "Missing course ID for update."}], 400

        existing_data = course_db_read_by_id(course_id)
        if not existing_data:
            return [], [{"message": f"Course ID {course_id} not found."}], 422

        if not isinstance(existing_data, dict):
            existing_data = course_row_to_dict(existing_data)

        full_data = {**existing_data, **incoming_data}

        try:
            row = course_dict_to_row(full_data)
            success = course_db_update(course_id, row)
            if success:
                updated_ids.append(course_id)
            else:
                errors.append({"message": f"Course ID {course_id} not updated."})
        except (ValueError, RuntimeError) as e:
            errors.append({"message": str(e)})

    if not updated_ids:
        return [], errors, 400

    updated_courses_rows = course_db_read_by_ids(updated_ids)
    updated_courses = [course_row_to_dict(row) for row in updated_courses_rows]

    return updated_courses, errors, 200


def archive_courses(ids):
    ids = normalize_to_list(ids)
    if not all(isinstance(item, int) for item in ids):
        return [], [{"message": "IDs must be integers"}], 400

    archived_ids = []
    errors = []

    for course_id in ids:
        rows_updated = course_db_archive(course_id)
        if rows_updated > 0:
            archived_ids.append(course_id)
        else:
            errors.append(
                {"message": f"Course ID {course_id} not found or already archived."}
            )

    if not archived_ids:
        return [], errors, 422

    # Read and return the updated records
    archived_rows = course_db_read_by_ids(archived_ids)
    archived_courses = [course_row_to_dict(row) for row in archived_rows]

    return archived_courses, errors, 200
