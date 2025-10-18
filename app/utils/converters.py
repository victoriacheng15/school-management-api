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


def department_dict_to_row(data):
    return (data.get("name", None),)


def program_dict_to_row(data):
    return (
        data.get("name", None),
        data.get("type", "diploma"),
        data.get("department_id"),
    )


def course_dict_to_row(data):
    return (
        data.get("title", None),
        data.get("code", None),
        data.get("term_id"),
        data.get("department_id"),
    )


def enrollment_dict_to_row(data):
    return (
        data.get("student_id"),
        data.get("course_id"),
        data.get("grade", None),
    )


def assignment_dict_to_row(data):
    return (
        data.get("instructor_id"),
        data.get("course_id"),
    )


def term_dict_to_row(data):
    return (
        data.get("name", None),
        data.get("start_date", None),
        data.get("end_date", None),
    )


def course_schedule_dict_to_row(data):
    return (
        data.get("course_id"),
        data.get("day"),
        data.get("time"),
        data.get("room", None),
    )
