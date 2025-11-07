from flask import Blueprint, jsonify, request
from app.utils import (
    build_bulk_response,
    api_response,
    api_response_error,
    handle_exceptions_read,
    handle_exceptions_write,
)
from app.services import (
    get_all_students,
    get_student_by_id,
    create_new_students,
    update_students,
    archive_students,
)

student_bp = Blueprint("student", __name__)


@student_bp.route("/api/students", methods=["GET"])
@handle_exceptions_read()
def handle_read_all_students():
    active_only = request.args.get("active_only", "false").lower() == "true"
    students = get_all_students(active_only=active_only)
    return api_response(students, "Students fetched successfully.")


@student_bp.route("/api/students/<int:student_id>", methods=["GET"])
@handle_exceptions_read()
def handle_get_student_by_id(student_id):
    student = get_student_by_id(student_id)
    if student is None:
        return api_response_error("Student not found.", 404)
    return api_response(student, "Student fetched successfully.")


@student_bp.route("/api/students", methods=["POST"])
@handle_exceptions_write()
def handle_create_student():
    results, error_data, status_code = create_new_students(request.get_json())

    if error_data:
        return api_response_error(error_data, status_code)

    response_data, status_code = build_bulk_response(
        success_list=results,
        success_msg_single="Student created successfully.",
        success_msg_bulk="{} students created successfully.",
        created=True,
    )
    return jsonify(response_data), status_code


@student_bp.route("/api/students", methods=["PUT"])
@handle_exceptions_write()
def handle_update_students():
    results, error_data, status_code = update_students(request.get_json())

    if error_data:
        return api_response_error(error_data, status_code)

    response_data, status_code = build_bulk_response(
        success_list=results,
        success_msg_single="Student updated successfully.",
        success_msg_bulk="{} students updated successfully.",
    )
    return jsonify(response_data), status_code


@student_bp.route("/api/students", methods=["PATCH"])
@handle_exceptions_write()
def handle_archive_students():
    payload = request.get_json()
    if not payload or "ids" not in payload:
        raise KeyError("ids")

    archived_data, error_data, status_code = archive_students(payload["ids"])

    if error_data:
        return api_response_error(error_data, status_code)

    response_data, status_code = build_bulk_response(
        success_list=archived_data,
        success_msg_single="Student archived successfully.",
        success_msg_bulk="{} students archived successfully.",
    )
    return jsonify(response_data), status_code
