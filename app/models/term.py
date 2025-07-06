from db.database import Database

db = Database()


def get_all_active_terms():
    query = "SELECT * FROM terms;"
    return db.execute_query(query)
