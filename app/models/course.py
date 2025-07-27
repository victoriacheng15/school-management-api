from db.database import Database

db = Database()


def course_db_read_all(active_only=False):
    query = "SELECT * FROM courses"
    if active_only:
        query += " WHERE is_archived = 0"
    query += ";"
    return db.execute_query(query)


def course_db_read_by_id(course_id):
    query = "SELECT * FROM courses WHERE id = ?;"
    result = db.execute_query(query, (course_id,))
    return result[0] if result else None


def course_db_read_by_ids(course_ids):
    if not course_ids:
        return []
    placeholders = ",".join("?" for _ in course_ids)
    query = f"SELECT * FROM courses WHERE id IN ({placeholders});"
    return db.execute_query(query, course_ids)


def course_db_insert(course_data):
    query = """
    INSERT INTO courses (
        title, code, term_id, department_id
    )
    VALUES (?, ?, ?, ?);
    """
    cursor = db.execute_query(query, course_data)
    return cursor.lastrowid if cursor else None


def course_db_update(course_id, course_data):
    query = """
    UPDATE courses
    SET title = ?, code = ?, term_id = ?, department_id = ?, updated_at = CURRENT_TIMESTAMP
    WHERE id = ? AND is_archived = 0;
    """
    values = course_data + (course_id,)
    cursor = db.execute_query(query, values)
    return cursor.rowcount if cursor else 0


def course_db_archive(course_id):
    query = """
    UPDATE courses
    SET is_archived = 1, updated_at = CURRENT_TIMESTAMP
    WHERE id = ? AND is_archived = 0;
    """
    cursor = db.execute_query(query, (course_id,))
    return cursor.rowcount if cursor else 0
