from db.database import Database
from db.db_utils import get_insert_returning_query, handle_insert_result, get_archived_condition, get_boolean_true

db = Database()


def student_db_read_all(active_only=False):
    query = "SELECT * FROM students"
    if active_only:
        query += " WHERE status = 'active'"
    query += ";"
    return db.execute_query(query)


def student_db_read_by_id(student_id):
    query = "SELECT * FROM students WHERE id = ?;"
    result = db.execute_query(query, (student_id,))
    return result[0] if result else None


def student_db_read_by_ids(student_ids):
    if not student_ids:
        return []
    placeholders = ",".join("?" for _ in student_ids)
    query = f"SELECT * FROM students WHERE id IN ({placeholders});"
    return db.execute_query(query, student_ids)


def student_db_insert(student_data):
    columns = [
        'first_name', 'last_name', 'email', 'address', 'city', 'province', 'country',
        'address_type', 'status', 'coop', 'is_international', 'program_id'
    ]
    query = get_insert_returning_query('students', columns)
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
