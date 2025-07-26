from db.database import Database

db = Database()


def department_db_read_all(active_only=False):
    query = "SELECT * FROM departments"
    if active_only:
        query += " WHERE is_archived = 0"
    query += ";"
    return db.execute_query(query)


def department_db_read_by_id(department_id):
    query = "SELECT * FROM departments WHERE id = ?;"
    result = db.execute_query(query, (department_id,))
    return result[0] if result else None


def department_db_read_by_ids(department_ids):
    if not department_ids:
        return []
    placeholders = ",".join("?" for _ in department_ids)
    query = f"SELECT * FROM departments WHERE id IN ({placeholders});"
    return db.execute_query(query, department_ids)


def department_db_insert(department_data):
    query = """
    INSERT INTO departments (name)
    VALUES (?);
    """
    cursor = db.execute_query(query, department_data)
    return cursor.lastrowid if cursor else None


def department_db_update(department_id, department_data):
    query = """
    UPDATE departments
    SET name = ?, updated_at = CURRENT_TIMESTAMP
    WHERE id = ? AND is_archived = 0;
    """
    values = department_data + (department_id,)
    cursor = db.execute_query(query, values)
    return cursor.rowcount if cursor else 0


def department_db_archive(department_id):
    query = """
    UPDATE departments
    SET is_archived = 1, updated_at = CURRENT_TIMESTAMP
    WHERE id = ? AND is_archived = 0;
    """
    cursor = db.execute_query(query, (department_id,))
    return cursor.rowcount if cursor else 0
