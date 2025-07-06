from db.database import Database

db = Database()


def get_all_active_course_schedules():
    query = "SELECT * FROM course_schedule WHERE is_archived = 0;"
    return db.execute_query(query)
