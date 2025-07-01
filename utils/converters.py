def student_row_to_dict(row):
    return {
        "id": row[0],
        "first_name": row[1],
        "last_name": row[2],
        "email": row[3],
        "address": row[4],
        "city": row[5],
        "province": row[6],
        "country": row[7],
        "address_type": row[8],
        "status": row[9],
        "coop": row[10],
        "is_international": row[11],
        "program_id": row[12],
        "created_at": row[13],
        "updated_at": row[14],
        "is_archived": row[15],
    }

def student_dict_to_row(data):
    return (
        data["first_name"],
        data["last_name"],
        data["email"],
        data.get("address", None),
        data.get("city", None),
        data.get("province", None),
        data.get("country", None),
        data.get("address_type", "local"), 
        data.get("status", "active"),
        data.get("coop", 0),
        data["is_international"],
        data.get("program_id", None),
    )

def instructor_row_to_dict(row):
    return {
        "id": row[0],
        "first_name": row[1],
        "last_name": row[2],
        "email": row[3],
        "address": row[4],
        "province": row[5],
        "employment": row[6],
        "status": row[7],
        "department_id": row[8],
        "created_at": row[9],
        "updated_at": row[10],
        "is_archived": row[11],
    }

def instructor_dict_to_row(data):
    return (
        data["first_name"], data["last_name"], data["email"], data["address"],
        data["province"], data["employment"], data["status"], data["department_id"]
    )

def department_row_to_dict(row):
    return {
        "id": row[0],
        "name": row[1],
        "created_at": row[2],
        "updated_at": row[3],
        "is_archived": row[4],
    }

def department_dict_to_row(data):
    return (data["name"],)

def program_row_to_dict(row):
    return {
        "id": row[0],
        "name": row[1],
        "type": row[2],
        "department_id": row[3],
        "created_at": row[4],
        "updated_at": row[5],
        "is_archived": row[6],
    }

def program_dict_to_row(data):
    return (data["name"], data["type"], data["department_id"])

def course_row_to_dict(row):
    return {
        "id": row[0],
        "title": row[1],
        "code": row[2],
        "term_id": row[3],
        "department_id": row[4],
        "created_at": row[5],
        "updated_at": row[6],
        "is_archived": row[7],
    }

def course_dict_to_row(data):
    return (data["title"], data["code"], data["term_id"], data["department_id"])

def enrollment_row_to_dict(row):
    return {
        "id": row[0],
        "student_id": row[1],
        "course_id": row[2],
        "grade": row[3],
        "created_at": row[4],
        "updated_at": row[5],
    }

def enrollment_dict_to_row(data):
    return (data["student_id"], data["course_id"], data["grade"])

def assignment_row_to_dict(row):
    return {
        "id": row[0],
        "instructor_id": row[1],
        "course_id": row[2],
        "created_at": row[3],
        "updated_at": row[4],
        "is_archived": row[5],
    }

def assignment_dict_to_row(data):
    return (data["instructor_id"], data["course_id"])

def term_row_to_dict(row):
    return {
        "id": row[0],
        "name": row[1],
        "start_date": row[2],
        "end_date": row[3],
        "created_at": row[4],
        "updated_at": row[5],
    }

def term_dict_to_row(data):
    return (data["name"], data["start_date"], data["end_date"])

def course_schedule_row_to_dict(row):
    return {
        "id": row[0],
        "course_id": row[1],
        "day": row[2],
        "time": row[3],
        "room": row[4],
        "created_at": row[5],
        "updated_at": row[6],
        "is_archived": row[7],
    }

def course_schedule_dict_to_row(data):
    return (data["course_id"], data["day"], data["time"], data["room"])
