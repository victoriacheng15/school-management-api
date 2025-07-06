from db.database import Database

db = Database()


def get_all_active_courses():
    query = "SELECT * FROM courses WHERE is_archived = 0;"
    return db.execute_query(query)
