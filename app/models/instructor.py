from db.database import Database

db = Database()


def get_all_active_instructors():
    query = "SELECT * FROM instructors WHERE status = 'active' AND is_archived = 0;"
    return db.execute_query(query)
