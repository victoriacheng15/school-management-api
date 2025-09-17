from db.database import Database
from db.db_utils import (
    get_insert_returning_query,
    handle_insert_result,
    get_archived_condition,
    get_boolean_true,
)

db = Database()


def program_db_read_all(active_only=False):
    query = "SELECT * FROM programs"
    if active_only:
        archived_condition = get_archived_condition(False)
        query += f" WHERE {archived_condition}"
    query += ";"
    result = db.execute_query(query)
    return [dict(row) for row in result] if result else []


def program_db_read_by_id(program_id):
    query = "SELECT * FROM programs WHERE id = %s;"
    result = db.execute_query(query, (program_id,))
    return dict(result[0]) if result else None


def program_db_read_by_ids(program_ids):
    if not program_ids:
        return []
    placeholders = ",".join("%s" for _ in program_ids)
    query = f"SELECT * FROM programs WHERE id IN ({placeholders});"
    result = db.execute_query(query, program_ids)
    return [dict(row) for row in result] if result else []


def program_db_insert(program_data):
    columns = ["name", "type", "department_id"]
    query = get_insert_returning_query("programs", columns)
    cursor_or_result = db.execute_query(query, program_data)
    return handle_insert_result(cursor_or_result)


def program_db_update(program_id, program_data):
    archived_condition = get_archived_condition(False)
    query = f"""
    UPDATE programs
    SET name = %s, type = %s, department_id = %s, updated_at = CURRENT_TIMESTAMP
    WHERE id = %s AND {archived_condition};
    """
    values = program_data + (program_id,)
    cursor = db.execute_query(query, values)
    return cursor.rowcount if cursor else 0


def program_db_archive(program_id):
    archived_condition_false = get_archived_condition(False)
    archived_true = get_boolean_true()
    query = f"""
    UPDATE programs
    SET is_archived = {archived_true}, updated_at = CURRENT_TIMESTAMP
    WHERE id = %s AND {archived_condition_false};
    """
    cursor = db.execute_query(query, (program_id,))
    return cursor.rowcount if cursor else 0
