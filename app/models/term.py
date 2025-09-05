from db.database import Database
from db.db_utils import (
    get_insert_returning_query,
    handle_insert_result,
    get_archived_condition,
    get_boolean_true,
)


db = Database()


def term_db_read_all(active_only=False):
    query = "SELECT * FROM terms"
    if active_only:
        archived_condition = get_archived_condition(False)
        query += f" WHERE {archived_condition}"
    query += ";"
    result = db.execute_query(query)
    # Convert rows to regular dicts for consistency with other models
    return [dict(row) for row in result] if result else []


def term_db_read_by_id(term_id):
    query = "SELECT * FROM terms WHERE id = ?;"
    result = db.execute_query(query, (term_id,))
    if result:
        return dict(result[0])
    return None


def term_db_read_by_ids(term_ids):
    if not term_ids:
        return []
    placeholders = ",".join("?" for _ in term_ids)
    query = f"SELECT * FROM terms WHERE id IN ({placeholders});"
    result = db.execute_query(query, term_ids)
    return [dict(row) for row in result] if result else []


def term_db_insert(term_data):
    columns = ["name", "start_date", "end_date"]
    query = get_insert_returning_query("terms", columns)
    cursor_or_result = db.execute_query(query, term_data)
    return handle_insert_result(cursor_or_result, cursor_or_result)


def term_db_update(term_id, term_data):
    archived_condition = get_archived_condition(False)
    query = f"""
    UPDATE terms
    SET name = ?, start_date = ?, end_date = ?, updated_at = CURRENT_TIMESTAMP
    WHERE id = ? AND {archived_condition};
    """
    values = term_data + (term_id,)
    cursor = db.execute_query(query, values)
    return cursor.rowcount if cursor else 0


def term_db_archive(term_id):
    archived_condition_false = get_archived_condition(False)
    archived_true = get_boolean_true()
    query = f"""
    UPDATE terms
    SET is_archived = {archived_true}, updated_at = CURRENT_TIMESTAMP
    WHERE id = ? AND {archived_condition_false};
    """
    cursor = db.execute_query(query, (term_id,))
    return cursor.rowcount if cursor else 0
