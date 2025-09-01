from db.database import Database
from db.db_utils import (
    get_insert_returning_query,
    handle_insert_result,
    get_archived_condition,
    get_boolean_true,
)

db = Database()


def instructor_db_read_all(active_only=False):
    query = "SELECT * FROM instructors"
    if active_only:
        query += " WHERE status = 'active'"
    query += ";"
    result = db.execute_query(query)
    # Convert all rows to regular dicts for consistency
    return [dict(row) for row in result] if result else []


def instructor_db_read_by_id(instructor_id):
    query = "SELECT * FROM instructors WHERE id = ?;"
    result = db.execute_query(query, (instructor_id,))
    if result:
        # Both SQLite and PostgreSQL return dict-like objects
        # result[0] is the first row (a dict-like object)
        return dict(result[0])  # Convert to regular dict for consistency
    return None


def instructor_db_read_by_ids(instructor_ids):
    if not instructor_ids:
        return []
    placeholders = ",".join("?" for _ in instructor_ids)
    query = f"SELECT * FROM instructors WHERE id IN ({placeholders});"
    result = db.execute_query(query, instructor_ids)
    # Convert all rows to regular dicts for consistency
    return [dict(row) for row in result] if result else []


def instructor_db_insert(instructor_data):
    columns = [
        "first_name",
        "last_name",
        "email",
        "address",
        "province",
        "employment",
        "status",
        "department_id",
    ]
    query = get_insert_returning_query("instructors", columns)
    cursor_or_result = db.execute_query(query, instructor_data)
    return handle_insert_result(cursor_or_result, cursor_or_result)


def instructor_db_update(instructor_id, instructor_data):
    archived_condition = get_archived_condition(False)
    query = f"""
    UPDATE instructors
    SET first_name = ?, last_name = ?, email = ?, address = ?, province = ?, employment = ?, status = ?, department_id = ?, updated_at = CURRENT_TIMESTAMP
    WHERE id = ? AND {archived_condition};
    """
    values = instructor_data + (instructor_id,)
    cursor = db.execute_query(query, values)
    return cursor.rowcount if cursor else 0


def instructor_db_archive(instructor_id):
    archived_condition_false = get_archived_condition(False)
    archived_true = get_boolean_true()
    query = f"""
    UPDATE instructors
    SET is_archived = {archived_true}, status = 'inactive', updated_at = CURRENT_TIMESTAMP
    WHERE id = ? AND {archived_condition_false};
    """
    cursor = db.execute_query(query, (instructor_id,))
    return cursor.rowcount if cursor else 0
