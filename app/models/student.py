from db.database import Database
from db.db_utils import (
    get_insert_returning_query,
    handle_insert_result,
    get_archived_condition,
    get_boolean_true,
)

db = Database()


def student_db_read_all(active_only=False):
    query = "SELECT * FROM students"
    if active_only:
        query += " WHERE status = 'active'"
    query += ";"
    result = db.execute_query(query)
    # Convert all rows to regular dicts for consistency
    return [dict(row) for row in result] if result else []


def student_db_read_by_id(student_id):
    query = "SELECT * FROM students WHERE id = ?;"
    result = db.execute_query(query, (student_id,))
    if result:
        # Both SQLite and PostgreSQL return dict-like objects
        # result[0] is the first row (a dict-like object)
        return dict(result[0])  # Convert to regular dict for consistency
    return None


def student_db_read_by_ids(student_ids):
    if not student_ids:
        return []
    placeholders = ",".join("?" for _ in student_ids)
    query = f"SELECT * FROM students WHERE id IN ({placeholders});"
    result = db.execute_query(query, student_ids)
    # Convert all rows to regular dicts for consistency
    return [dict(row) for row in result] if result else []


def student_db_insert(student_data):
    columns = [
        "first_name",
        "last_name",
        "email",
        "address",
        "city",
        "province",
        "country",
        "address_type",
        "status",
        "coop",
        "is_international",
        "program_id",
    ]
    query = get_insert_returning_query("students", columns)
    print(f"DEBUG: Insert query: {query}")
    print(f"DEBUG: Student data: {student_data}")
    cursor_or_result = db.execute_query(query, student_data)
    return handle_insert_result(cursor_or_result, cursor_or_result)


def student_db_update(student_id, student_data):
    archived_condition = get_archived_condition(False)
    query = f"""
    UPDATE students
    SET first_name = ?, last_name = ?, email = ?, address = ?, city = ?, province = ?, country = ?,
        address_type = ?, status = ?, coop = ?, is_international = ?, program_id = ?, updated_at = CURRENT_TIMESTAMP
    WHERE id = ? AND {archived_condition};
    """
    values = student_data + (student_id,)
    cursor = db.execute_query(query, values)
    return cursor.rowcount if cursor else 0


def student_db_archive(student_id):
    archived_condition_false = get_archived_condition(False)
    archived_true = get_boolean_true()
    query = f"""
    UPDATE students
    SET is_archived = {archived_true}, status = 'inactive', updated_at = CURRENT_TIMESTAMP
    WHERE id = ? AND {archived_condition_false};
    """
    cursor = db.execute_query(query, (student_id,))
    return cursor.rowcount if cursor else 0
