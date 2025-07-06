from db.database import Database

db = Database()


def get_all_active_enrollments():
    query = "SELECT * FROM enrollments;"
    return db.execute_query(query)
