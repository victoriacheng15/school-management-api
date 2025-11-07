from flask import Blueprint, jsonify, request
from app.utils import (
    build_bulk_response,
    api_response,
    api_response_error,
    handle_exceptions_read,
    handle_exceptions_write,
)
from app.services import (
    get_all_courses,
    get_course_by_id,
    create_new_courses,
    update_courses,
    archive_courses,
)

course_bp = Blueprint("course", __name__)


@course_bp.route("/api/courses", methods=["GET"])
@handle_exceptions_read()
def handle_read_all_courses():
    active_only = request.args.get("active_only", "false").lower() == "true"
    courses = get_all_courses(active_only=active_only)
    return api_response(courses, "Courses fetched successfully.")


@course_bp.route("/api/courses/<int:course_id>", methods=["GET"])
@handle_exceptions_read()
def handle_get_course_by_id(course_id):
    course = get_course_by_id(course_id)
    if course is None:
        return api_response_error("Course not found.", 404)
    return api_response(course, "Course fetched successfully.")


@course_bp.route("/api/courses", methods=["POST"])
@handle_exceptions_write()
def handle_create_course():
    results, error_data, status_code = create_new_courses(request.get_json())

    if error_data:
        return api_response_error(error_data, status_code)

    response_data, status_code = build_bulk_response(
        success_list=results,
        success_msg_single="Course created successfully.",
        success_msg_bulk="{} courses created successfully.",
        created=True,
    )
    return jsonify(response_data), status_code


@course_bp.route("/api/courses", methods=["PUT"])
@handle_exceptions_write()
def handle_update_courses():
    results, error_data, status_code = update_courses(request.get_json())

    if error_data:
        return api_response_error(error_data, status_code)

    response_data, status_code = build_bulk_response(
        success_list=results,
        success_msg_single="Course updated successfully.",
        success_msg_bulk="{} courses updated successfully.",
    )
    return jsonify(response_data), status_code


@course_bp.route("/api/courses", methods=["PATCH"])
@handle_exceptions_write()
def handle_archive_courses():
    payload = request.get_json()
    if not payload or "ids" not in payload:
        raise KeyError("ids")

    archived_data, error_data, status_code = archive_courses(payload["ids"])

    if error_data:
        return api_response_error(error_data, status_code)

    response_data, status_code = build_bulk_response(
        success_list=archived_data,
        success_msg_single="Course archived successfully.",
        success_msg_bulk="{} courses archived successfully.",
    )
    return jsonify(response_data), status_code
