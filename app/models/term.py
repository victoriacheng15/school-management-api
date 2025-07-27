from db.database import Database

db = Database()


def term_db_read_all():
    query = "SELECT * FROM terms;"
    return db.execute_query(query)


def term_db_read_by_id(term_id):
    query = "SELECT * FROM terms WHERE id = ?;"
    result = db.execute_query(query, (term_id,))
    return result[0] if result else None


def term_db_read_by_ids(term_ids):
    if not term_ids:
        return []
    placeholders = ",".join("?" for _ in term_ids)
    query = f"SELECT * FROM terms WHERE id IN ({placeholders});"
    return db.execute_query(query, term_ids)


def term_db_insert(term_data):
    query = """
    INSERT INTO terms (
        name, start_date, end_date
    )
    VALUES (?, ?, ?);
    """
    cursor = db.execute_query(query, term_data)
    return cursor.lastrowid if cursor else None


def term_db_update(term_id, term_data):
    query = """
    UPDATE terms
    SET name = ?, start_date = ?, end_date = ?, updated_at = CURRENT_TIMESTAMP
    WHERE id = ?;
    """
    values = term_data + (term_id,)
    cursor = db.execute_query(query, values)
    return cursor.rowcount if cursor else 0