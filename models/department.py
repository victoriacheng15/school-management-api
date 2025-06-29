from db.database import Database

db = Database()

def get_all_active_departments():
    query = "SELECT * FROM departments WHERE is_archived = 0;"
    return db.execute_query(query)