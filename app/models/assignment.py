from db.database import Database
from db.db_utils import (
    get_insert_returning_query,
    handle_insert_result,
    get_archived_condition,
    BOOLEAN_TRUE,
)

db = Database()


def assignment_db_read_all(active_only=False):
    query = "SELECT * FROM assignments"
    if active_only:
        query += f" WHERE {get_archived_condition()}"
    query += ";"
    result = db.execute_query(query)
    # Convert all rows to regular dicts for consistency
    return [dict(row) for row in result] if result else []


def assignment_db_read_by_id(assignment_id):
    query = "SELECT * FROM assignments WHERE id = ?;"
    result = db.execute_query(query, (assignment_id,))
    return dict(result[0]) if result else None


def assignment_db_read_by_ids(assignment_ids):
    if not assignment_ids:
        return []
    placeholders = ",".join("?" for _ in assignment_ids)
    query = f"SELECT * FROM assignments WHERE id IN ({placeholders});"
    result = db.execute_query(query, assignment_ids)
    return [dict(row) for row in result] if result else []


def assignment_db_insert(assignment_data):
    columns = ["instructor_id", "course_id"]
    query = get_insert_returning_query("assignments", columns)
    cursor_or_result = db.execute_query(query, assignment_data)
    return handle_insert_result(cursor_or_result)


def assignment_db_update(assignment_id, assignment_data):
    archived_condition = get_archived_condition(False)
    query = f"""
    UPDATE assignments
    SET instructor_id = ?, course_id = ?, updated_at = CURRENT_TIMESTAMP
    WHERE id = ? AND {archived_condition};
    """
    values = assignment_data + (assignment_id,)
    cursor = db.execute_query(query, values)
    return cursor.rowcount if cursor else 0


def assignment_db_archive(assignment_id):
    archived_condition_false = get_archived_condition(False)
    query = f"""
    UPDATE assignments
    SET is_archived = {BOOLEAN_TRUE}, updated_at = CURRENT_TIMESTAMP
    WHERE id = ? AND {archived_condition_false};
    """
    cursor = db.execute_query(query, (assignment_id,))
    return cursor.rowcount if cursor else 0
