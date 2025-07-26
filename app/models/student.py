from db.database import Database

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
    query = """
    INSERT INTO students (
        first_name, last_name, email, address, city, province, country,
        address_type, status, coop, is_international, program_id
    )
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);
    """
    cursor = db.execute_query(query, student_data)
    return cursor.lastrowid if cursor else None


def student_db_update(student_id, student_data):
    query = """
    UPDATE students
    SET first_name = ?, last_name = ?, email = ?, address = ?, city = ?, province = ?, country = ?,
        address_type = ?, status = ?, coop = ?, is_international = ?, program_id = ?, updated_at = CURRENT_TIMESTAMP
    WHERE id = ? AND is_archived = 0;
    """
    values = student_data + (student_id,)
    cursor = db.execute_query(query, values)
    return cursor.rowcount if cursor else 0


def student_db_archive(student_id):
    query = """
    UPDATE students
    SET is_archived = 1, status = 'inactive', updated_at = CURRENT_TIMESTAMP
    WHERE id = ? AND is_archived = 0;
    """
    cursor = db.execute_query(query, (student_id,))
    return cursor.rowcount if cursor else 0
