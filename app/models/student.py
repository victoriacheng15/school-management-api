from db.database import Database

db = Database()


def read_all_active_students():
    query = "SELECT * FROM students WHERE status = 'active';"
    return db.execute_query(query)


def read_student_by_id(student_id):
    query = "SELECT * FROM students WHERE id = ?;"
    result = db.execute_query(query, (student_id,))
    if result and len(result) > 0:
        return result[0]
    return None


def create_student(student_data):
    query = """
    INSERT INTO students (
        first_name, last_name, email, address, city, province, country,
        address_type, status, coop, is_international, program_id
    )
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);
    """
    cursor = db.execute_query(query, student_data)
    if cursor:
        return cursor.lastrowid
    return None

def update_student(student_id, student_data):
    query = """
    UPDATE students
    SET first_name = ?, last_name = ?, email = ?, address = ?, city = ?, province = ?, country = ?,
        address_type = ?, status = ?, coop = ?, is_international = ?, program_id = ?, updated_at = CURRENT_TIMESTAMP
    WHERE id = ? AND is_archived = 0;
    """
    values = student_data + (student_id,)
    cursor = db.execute_query(query, values)
    return cursor.rowcount if cursor else 0

def archive_student(student_id):
    query = """
    UPDATE students
    SET is_archived = 1, updated_at = CURRENT_TIMESTAMP
    WHERE id = ? AND is_archived = 0;
    """
    cursor = db.execute_query(query, (student_id,))
    return cursor.rowcount if cursor else 0