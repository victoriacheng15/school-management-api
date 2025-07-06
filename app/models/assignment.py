from db.database import Database

db = Database()

def get_all_active_assignments():
    query = "SELECT * FROM assignments WHERE is_archived = 0;"
    return db.execute_query(query)