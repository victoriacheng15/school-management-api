from db.database import Database

db = Database()


def enrollment_db_read_all():
    query = "SELECT * FROM enrollments;"
    return db.execute_query(query)


def enrollment_db_read_by_id(enrollment_id):
    query = "SELECT * FROM enrollments WHERE id = ?;"
    result = db.execute_query(query, (enrollment_id,))
    return result[0] if result else None


def enrollment_db_read_by_ids(enrollment_ids):
    if not enrollment_ids:
        return []
    placeholders = ",".join("?" for _ in enrollment_ids)
    query = f"SELECT * FROM enrollments WHERE id IN ({placeholders});"
    return db.execute_query(query, enrollment_ids)


def enrollment_db_insert(enrollment_data):
    query = """
    INSERT INTO enrollments (
        student_id, course_id, grade
    )
    VALUES (?, ?, ?);
    """
    cursor = db.execute_query(query, enrollment_data)
    return cursor.lastrowid if cursor else None


def enrollment_db_update(enrollment_id, enrollment_data):
    query = """
    UPDATE enrollments
    SET student_id = ?, course_id = ?, grade = ?, updated_at = CURRENT_TIMESTAMP
    WHERE id = ?;
    """
    values = enrollment_data + (enrollment_id,)
    cursor = db.execute_query(query, values)
    return cursor.rowcount if cursor else 0