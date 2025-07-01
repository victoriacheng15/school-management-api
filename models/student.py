from db.database import Database

db = Database()

def get_all_active_students():
    query = "SELECT * FROM students WHERE status = 'active';"
    return db.execute_query(query)

def get_student_by_id(student_id):
    query = "SELECT * FROM students WHERE id = ?;"
    result = db.execute_query(query, (student_id,))
    if result and len(result) > 0:
        return result[0]
    return None

def insert_student(student_data):
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