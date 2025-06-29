from db.database import Database

db = Database()

def get_all_active_students():
    query = "SELECT * FROM students WHERE status = 'active' AND is_archived = 0;"
    return db.execute_query(query)
