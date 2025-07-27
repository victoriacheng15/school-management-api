from db.database import Database

db = Database()


def course_schedule_db_read_all(active_only=False):
    query = "SELECT * FROM course_schedule"
    if active_only:
        query += " WHERE is_archived = 0"
    query += ";"
    return db.execute_query(query)


def course_schedule_db_read_by_id(course_schedule_id):
    query = "SELECT * FROM course_schedule WHERE id = ?;"
    result = db.execute_query(query, (course_schedule_id,))
    return result[0] if result else None


def course_schedule_db_read_by_ids(course_schedule_ids):
    if not course_schedule_ids:
        return []
    placeholders = ",".join("?" for _ in course_schedule_ids)
    query = f"SELECT * FROM course_schedule WHERE id IN ({placeholders});"
    return db.execute_query(query, course_schedule_ids)


def course_schedule_db_insert(course_schedule_data):
    query = """
    INSERT INTO course_schedule (
        course_id, day, time, room
    )
    VALUES (?, ?, ?, ?);
    """
    cursor = db.execute_query(query, course_schedule_data)
    return cursor.lastrowid if cursor else None


def course_schedule_db_update(course_schedule_id, course_schedule_data):
    query = """
    UPDATE course_schedule
    SET course_id = ?, day = ?, time = ?, room = ?, updated_at = CURRENT_TIMESTAMP
    WHERE id = ? AND is_archived = 0;
    """
    values = course_schedule_data + (course_schedule_id,)
    cursor = db.execute_query(query, values)
    return cursor.rowcount if cursor else 0


def course_schedule_db_archive(course_schedule_id):
    query = """
    UPDATE course_schedule
    SET is_archived = 1, updated_at = CURRENT_TIMESTAMP
    WHERE id = ? AND is_archived = 0;
    """
    cursor = db.execute_query(query, (course_schedule_id,))
    return cursor.rowcount if cursor else 0