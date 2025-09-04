def student_row_to_dict(row):
    return {
        "id": row["id"],
        "first_name": row["first_name"],
        "last_name": row["last_name"],
        "email": row["email"],
        "address": row["address"],
        "city": row["city"],
        "province": row["province"],
        "country": row["country"],
        "address_type": row["address_type"],
        "status": row["status"],
        "coop": row["coop"],
        "is_international": row["is_international"],
        "program_id": row["program_id"],
        "created_at": row["created_at"],
        "updated_at": row["updated_at"],
        "is_archived": row["is_archived"],
    }


def student_dict_to_row(data):
    return (
        data.get("first_name", None),
        data.get("last_name", None),
        data.get("email", None),
        data.get("address"),
        data.get("city"),
        data.get("province"),
        data.get("country"),
        data.get("address_type", "local"),
        data.get("status", "active"),
        bool(data.get("coop", 0)),
        bool(data.get("is_international", 0)),
        data.get("program_id"),
    )


def instructor_row_to_dict(row):
    return {
        "id": row["id"],
        "first_name": row["first_name"],
        "last_name": row["last_name"],
        "email": row["email"],
        "address": row["address"],
        "province": row["province"],
        "employment": row["employment"],
        "status": row["status"],
        "department_id": row["department_id"],
        "created_at": row["created_at"],
        "updated_at": row["updated_at"],
        "is_archived": row["is_archived"],
    }


def instructor_dict_to_row(data):
    return (
        data.get("first_name", None),
        data.get("last_name", None),
        data.get("email", None),
        data.get("address"),
        data.get("province"),
        data.get("employment", "full-time"),
        data.get("status", "active"),
        data.get("department_id"),
    )


def department_row_to_dict(row):
    return {
        "id": row["id"],
        "name": row["name"],
        "created_at": row.get("created_at"),
        "updated_at": row.get("updated_at"),
        "is_archived": row.get("is_archived"),
    }


def department_dict_to_row(data):
    return (data.get("name", None),)


def program_row_to_dict(row):
    return {
        "id": row["id"],
        "name": row["name"],
        "type": row["type"],
        "department_id": row.get("department_id"),
        "created_at": row.get("created_at"),
        "updated_at": row.get("updated_at"),
        "is_archived": row.get("is_archived"),
    }


def program_dict_to_row(data):
    return (
        data.get("name", None),
        data.get("type", "diploma"),
        data.get("department_id"),
    )


def course_row_to_dict(row):
    return {
        "id": row["id"],
        "title": row["title"],
        "code": row["code"],
        "term_id": row["term_id"],
        "department_id": row["department_id"],
        "created_at": row.get("created_at"),
        "updated_at": row.get("updated_at"),
        "is_archived": row.get("is_archived"),
    }


def course_dict_to_row(data):
    return (
        data.get("title", None),
        data.get("code", None),
        data.get("term_id"),
        data.get("department_id"),
    )


def enrollment_row_to_dict(row):
    return {
        "id": row["id"],
        "student_id": row["student_id"],
        "course_id": row["course_id"],
        "grade": row["grade"],
        "created_at": row["created_at"],
        "updated_at": row["updated_at"],
        "is_archived": row["is_archived"],
    }


def enrollment_dict_to_row(data):
    return (
        data.get("student_id"),
        data.get("course_id"),
        data.get("grade", None),
    )


def assignment_row_to_dict(row):
    return {
        "id": row["id"],
        "instructor_id": row["instructor_id"],
        "course_id": row["course_id"],
        "created_at": row["created_at"],
        "updated_at": row["updated_at"],
        "is_archived": row["is_archived"],
    }


def assignment_dict_to_row(data):
    return (
        data.get("instructor_id"),
        data.get("course_id"),
    )


def term_row_to_dict(row):
    return {
        "id": row["id"],
        "name": row["name"],
        "start_date": row["start_date"],
        "end_date": row["end_date"],
        "created_at": row.get("created_at"),
        "updated_at": row.get("updated_at"),
    }


def term_dict_to_row(data):
    return (
        data.get("name", None),
        data.get("start_date", None),
        data.get("end_date", None),
    )


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
    return (
        data.get("course_id"),
        data.get("day"),
        data.get("time"),
        data.get("room", None),
    )
