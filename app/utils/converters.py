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
        data.get("first_name", None),
        data.get("last_name", None),
        data.get("email", None),
        data.get("address"),
        data.get("city"),
        data.get("province"),
        data.get("country"),
        data.get("address_type", "local"),
        data.get("status", "active"),
        int(bool(data.get("coop", 0))),
        int(bool(data.get("is_international", 0))),
        data.get("program_id"),
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
        "id": row[0],
        "name": row[1],
        "created_at": row[2],
        "updated_at": row[3],
        "is_archived": row[4],
    }


def department_dict_to_row(data):
    return (data.get("name", None),)


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
    return (
        data.get("name", None),
        data.get("type", "diploma"),
        data.get("department_id"),
    )


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
    return (
        data.get("title", None),
        data.get("code", None),
        data.get("term_id"),
        data.get("department_id"),
    )


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
    return (
        data.get("student_id"),
        data.get("course_id"),
        data.get("grade", None),
    )




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
    return (
        data.get("instructor_id"),
        data.get("course_id"),
    )


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
