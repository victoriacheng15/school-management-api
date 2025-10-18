from db.database import Database
from db.db_utils import (
    get_insert_returning_query,
    handle_insert_result,
    get_archived_condition,
    BOOLEAN_TRUE,
)

db = Database()


def course_db_read_all(active_only=False):
    query = "SELECT * FROM courses"
    if active_only:
        archived_condition = get_archived_condition(False)
        query += f" WHERE {archived_condition}"
    query += ";"
    result = db.execute_query(query)
    return [dict(row) for row in result] if result else []


def course_db_read_by_id(course_id):
    query = "SELECT * FROM courses WHERE id = %s;"
    result = db.execute_query(query, (course_id,))
    return dict(result[0]) if result else None


def course_db_read_by_ids(course_ids):
    if not course_ids:
        return []
    placeholders = ",".join("%s" for _ in course_ids)
    query = f"SELECT * FROM courses WHERE id IN ({placeholders});"
    result = db.execute_query(query, course_ids)
    return [dict(row) for row in result] if result else []


def course_db_insert(course_data):
    columns = ["title", "code", "term_id", "department_id"]
    query = get_insert_returning_query("courses", columns)
    cursor_or_result = db.execute_query(query, course_data)
    return handle_insert_result(cursor_or_result)


def course_db_update(course_id, course_data):
    archived_condition = get_archived_condition(False)
    query = f"""
    UPDATE courses
    SET title = %s, code = %s, term_id = %s, department_id = %s, updated_at = CURRENT_TIMESTAMP
    WHERE id = %s AND {archived_condition};
    """
    values = course_data + (course_id,)
    cursor = db.execute_query(query, values)
    return cursor.rowcount if cursor else 0


def course_db_archive(course_id):
    archived_condition_false = get_archived_condition(False)
    query = f"""
    UPDATE courses
    SET is_archived = {BOOLEAN_TRUE}, updated_at = CURRENT_TIMESTAMP
    WHERE id = %s AND {archived_condition_false};
    """
    cursor = db.execute_query(query, (course_id,))
    return cursor.rowcount if cursor else 0
