from db.database import Database
from db.db_utils import (
    get_insert_returning_query,
    handle_insert_result,
    get_archived_condition,
    BOOLEAN_TRUE,
)

db = Database()


def enrollment_db_read_all(active_only=False):
    query = "SELECT * FROM enrollments"
    if active_only:
        archived_condition = get_archived_condition(False)
        query += f" WHERE {archived_condition}"
    query += ";"
    result = db.execute_query(query)
    return [dict(row) for row in result] if result else []


def enrollment_db_read_by_id(enrollment_id):
    query = "SELECT * FROM enrollments WHERE id = %s;"
    result = db.execute_query(query, (enrollment_id,))
    return dict(result[0]) if result else None


def enrollment_db_read_by_ids(enrollment_ids):
    if not enrollment_ids:
        return []
    placeholders = ",".join("%s" for _ in enrollment_ids)
    query = f"SELECT * FROM enrollments WHERE id IN ({placeholders});"
    result = db.execute_query(query, enrollment_ids)
    return [dict(row) for row in result] if result else []


def enrollment_db_insert(enrollment_data):
    columns = ["student_id", "course_id", "grade"]
    query = get_insert_returning_query("enrollments", columns)
    cursor_or_result = db.execute_query(query, enrollment_data)
    return handle_insert_result(cursor_or_result)


def enrollment_db_update(enrollment_id, enrollment_data):
    archived_condition = get_archived_condition(False)
    query = f"""
    UPDATE enrollments
    SET student_id = %s, course_id = %s, grade = %s, updated_at = CURRENT_TIMESTAMP
    WHERE id = %s AND {archived_condition};
    """
    values = enrollment_data + (enrollment_id,)
    cursor = db.execute_query(query, values)
    return cursor.rowcount if cursor else 0


def enrollment_db_archive(enrollment_id):
    archived_condition_false = get_archived_condition(False)
    query = f"""
    UPDATE enrollments
    SET is_archived = {BOOLEAN_TRUE}, updated_at = CURRENT_TIMESTAMP
    WHERE id = %s AND {archived_condition_false};
    """
    cursor = db.execute_query(query, (enrollment_id,))
    return cursor.rowcount if cursor else 0
