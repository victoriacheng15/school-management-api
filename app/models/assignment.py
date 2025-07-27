from db.database import Database

db = Database()


def assignment_db_read_all(active_only=False):
    query = "SELECT * FROM assignments"
    if active_only:
        query += " WHERE is_archived = 0"
    query += ";"
    return db.execute_query(query)


def assignment_db_read_by_id(assignment_id):
    query = "SELECT * FROM assignments WHERE id = ?;"
    result = db.execute_query(query, (assignment_id,))
    return result[0] if result else None


def assignment_db_read_by_ids(assignment_ids):
    if not assignment_ids:
        return []
    placeholders = ",".join("?" for _ in assignment_ids)
    query = f"SELECT * FROM assignments WHERE id IN ({placeholders});"
    return db.execute_query(query, assignment_ids)


def assignment_db_insert(assignment_data):
    query = """
    INSERT INTO assignments (
        instructor_id, course_id
    )
    VALUES (?, ?);
    """
    cursor = db.execute_query(query, assignment_data)
    return cursor.lastrowid if cursor else None


def assignment_db_update(assignment_id, assignment_data):
    query = """
    UPDATE assignments
    SET instructor_id = ?, course_id = ?, updated_at = CURRENT_TIMESTAMP
    WHERE id = ? AND is_archived = 0;
    """
    values = assignment_data + (assignment_id,)
    cursor = db.execute_query(query, values)
    return cursor.rowcount if cursor else 0


def assignment_db_archive(assignment_id):
    query = """
    UPDATE assignments
    SET is_archived = 1, updated_at = CURRENT_TIMESTAMP
    WHERE id = ? AND is_archived = 0;
    """
    cursor = db.execute_query(query, (assignment_id,))
    return cursor.rowcount if cursor else 0
