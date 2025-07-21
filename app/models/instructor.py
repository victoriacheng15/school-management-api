from db.database import Database

db = Database()


def instructor_db_read_all(active_only=False):
    query = "SELECT * FROM instructors"
    if active_only:
        query += " WHERE status = 'active'"
    query += ";"
    return db.execute_query(query)


def instructor_db_read_by_id(instructor_id):
    query = "SELECT * FROM instructors WHERE id = ?;"
    result = db.execute_query(query, (instructor_id,))
    if result and len(result) > 0:
        return result[0]
    return None


def instructor_db_read_by_ids(instructor_ids):
    if not instructor_ids:
        return []
    placeholders = ",".join("?" for _ in instructor_ids)
    query = f"SELECT * FROM instructors WHERE id IN ({placeholders});"
    return db.execute_query(query, instructor_ids)


def instructor_db_insert(instructor_data):
    query = """
    INSERT INTO instructors (
        first_name, last_name, email, address, province, employment,
        status, department_id
    )
    VALUES (?, ?, ?, ?, ?, ?, ?, ?);
    """
    cursor = db.execute_query(query, instructor_data)
    return cursor.lastrowid if cursor else None


def instructor_db_update(instructor_id, instructor_data):
    query = """
    UPDATE instructors
    SET first_name = ?, last_name = ?, email = ?, address = ?, province = ?,
        employment = ?, status = ?, department_id = ?, updated_at = CURRENT_TIMESTAMP
    WHERE id = ? AND is_archived = 0;
    """
    values = instructor_data + (instructor_id,)
    cursor = db.execute_query(query, values)
    return cursor.rowcount if cursor else 0


def instructor_db_archive(instructor_id):
    query = """
    UPDATE instructors
    SET is_archived = 1, status = 'inactive', updated_at = CURRENT_TIMESTAMP
    WHERE id = ? AND is_archived = 0;
    """
    cursor = db.execute_query(query, (instructor_id,))
    return cursor.rowcount if cursor else 0
