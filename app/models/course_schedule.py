from db.database import Database
from db.db_utils import (
    get_insert_returning_query,
    handle_insert_result,
    get_archived_condition,
    BOOLEAN_TRUE,
)

db = Database()


def course_schedule_db_read_all(active_only=False):
    query = "SELECT * FROM course_schedule"
    if active_only:
        # use archived condition helper for DB portability
        archived_condition = get_archived_condition(False)
        query += f" WHERE {archived_condition}"
    query += ";"
    result = db.execute_query(query)
    # Convert all rows to regular dicts for consistency
    return [dict(row) for row in result] if result else []


def course_schedule_db_read_by_id(course_schedule_id):
    query = "SELECT * FROM course_schedule WHERE id = %s;"
    result = db.execute_query(query, (course_schedule_id,))
    return dict(result[0]) if result else None


def course_schedule_db_read_by_ids(course_schedule_ids):
    if not course_schedule_ids:
        return []
    placeholders = ",".join("%s" for _ in course_schedule_ids)
    query = f"SELECT * FROM course_schedule WHERE id IN ({placeholders});"
    result = db.execute_query(query, course_schedule_ids)
    return [dict(row) for row in result] if result else []


def course_schedule_db_insert(course_schedule_data):
    columns = ["course_id", "day", "time", "room"]
    query = get_insert_returning_query("course_schedule", columns)
    cursor_or_result = db.execute_query(query, course_schedule_data)
    return handle_insert_result(cursor_or_result)


def course_schedule_db_update(course_schedule_id, course_schedule_data):
    archived_condition = get_archived_condition(False)
    query = f"""
    UPDATE course_schedule
    SET course_id = %s, day = %s, time = %s, room = %s, updated_at = CURRENT_TIMESTAMP
    WHERE id = %s AND {archived_condition};
    """
    values = course_schedule_data + (course_schedule_id,)
    cursor = db.execute_query(query, values)
    return cursor.rowcount if cursor else 0


def course_schedule_db_archive(course_schedule_id):
    archived_condition_false = get_archived_condition(False)
    query = f"""
    UPDATE course_schedule
    SET is_archived = {BOOLEAN_TRUE}, updated_at = CURRENT_TIMESTAMP
    WHERE id = %s AND {archived_condition_false};
    """
    cursor = db.execute_query(query, (course_schedule_id,))
    return cursor.rowcount if cursor else 0
