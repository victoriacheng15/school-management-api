from db.database import Database
from db.db_utils import (
    get_insert_returning_query,
    handle_insert_result,
    get_archived_condition,
    get_boolean_true,
)


db = Database()


def department_db_read_all(active_only=False):
    query = "SELECT * FROM departments"
    if active_only:
        archived_condition = get_archived_condition(False)
        query += f" WHERE {archived_condition}"
    query += ";"
    result = db.execute_query(query)
    return [dict(row) for row in result] if result else []


def department_db_read_by_id(department_id):
    query = "SELECT * FROM departments WHERE id = ?;"
    result = db.execute_query(query, (department_id,))
    return dict(result[0]) if result else None


def department_db_read_by_ids(department_ids):
    if not department_ids:
        return []
    placeholders = ",".join("?" for _ in department_ids)
    query = f"SELECT * FROM departments WHERE id IN ({placeholders});"
    result = db.execute_query(query, department_ids)
    return [dict(row) for row in result] if result else []


def department_db_insert(department_data):
    columns = ["name"]
    query = get_insert_returning_query("departments", columns)
    cursor_or_result = db.execute_query(query, department_data)
    return handle_insert_result(cursor_or_result, cursor_or_result)


def department_db_update(department_id, department_data):
    archived_condition = get_archived_condition(False)
    query = f"""
    UPDATE departments
    SET name = ?, updated_at = CURRENT_TIMESTAMP
    WHERE id = ? AND {archived_condition};
    """
    values = department_data + (department_id,)
    cursor = db.execute_query(query, values)
    return cursor.rowcount if cursor else 0


def department_db_archive(department_id):
    archived_condition_false = get_archived_condition(False)
    archived_true = get_boolean_true()
    query = f"""
    UPDATE departments
    SET is_archived = {archived_true}, updated_at = CURRENT_TIMESTAMP
    WHERE id = ? AND {archived_condition_false};
    """
    cursor = db.execute_query(query, (department_id,))
    return cursor.rowcount if cursor else 0
