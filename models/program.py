from db.database import Database

db = Database()

def get_all_active_programs():
    query = "SELECT * FROM programs WHERE is_archived = 0;"
    return db.execute_query(query)