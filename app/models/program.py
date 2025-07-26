from db.database import Database

db = Database()


def program_db_read_all(active_only=False):
    query = "SELECT * FROM programs"
    if active_only:
        query += " WHERE is_archived = 0"
    query += ";"
    return db.execute_query(query)


def program_db_read_by_id(program_id):
    query = "SELECT * FROM programs WHERE id = ?;"
    result = db.execute_query(query, (program_id,))
    return result[0] if result else None


def program_db_read_by_ids(program_ids):
    if not program_ids:
        return []
    placeholders = ",".join("?" for _ in program_ids)
    query = f"SELECT * FROM programs WHERE id IN ({placeholders});"
    return db.execute_query(query, program_ids)


def program_db_insert(program_data):
    query = """
    INSERT INTO programs (
        name, type, department_id
    )
    VALUES (?, ?, ?);
    """
    cursor = db.execute_query(query, program_data)
    return cursor.lastrowid if cursor else None


def program_db_update(program_id, program_data):
    query = """
    UPDATE programs
    SET name = ?, type = ?, department_id = ?, updated_at = CURRENT_TIMESTAMP
    WHERE id = ? AND is_archived = 0;
    """
    values = program_data + (program_id,)
    cursor = db.execute_query(query, values)
    return cursor.rowcount if cursor else 0


def program_db_archive(program_id):
    query = """
    UPDATE programs
    SET is_archived = 1, updated_at = CURRENT_TIMESTAMP
    WHERE id = ? AND is_archived = 0;
    """
    cursor = db.execute_query(query, (program_id,))
    return cursor.rowcount if cursor else 0
