from flask import Blueprint, jsonify, request
from app.utils import (
    build_bulk_response,
    api_response,
    api_response_error,
    handle_exceptions_read,
    handle_exceptions_write,
)
from app.services import (
    get_all_instructors,
    get_instructor_by_id,
    create_new_instructors,
    update_instructors,
    archive_instructors,
)

instructor_bp = Blueprint("instructor", __name__)


@instructor_bp.route("/api/instructors", methods=["GET"])
@handle_exceptions_read()
def handle_read_all_instructors():
    active_only = request.args.get("active_only", "false").lower() == "true"
    instructors = get_all_instructors(active_only=active_only)
    return api_response(instructors, "Instructors fetched successfully.")


@instructor_bp.route("/api/instructors/<int:instructor_id>", methods=["GET"])
@handle_exceptions_read()
def handle_get_instructor_by_id(instructor_id):
    instructor = get_instructor_by_id(instructor_id)
    if instructor is None:
        return api_response_error("Instructor not found.", 404)
    return api_response(instructor, "Instructor fetched successfully.")


@instructor_bp.route("/api/instructors", methods=["POST"])
@handle_exceptions_write()
def handle_create_instructor():
    results, error_data, status_code = create_new_instructors(request.get_json())

    if error_data:
        return api_response_error(error_data, status_code)

    response_data, status_code = build_bulk_response(
        success_list=results,
        success_msg_single="Instructor created successfully.",
        success_msg_bulk="{} instructors created successfully.",
        created=True,
    )
    return jsonify(response_data), status_code


@instructor_bp.route("/api/instructors", methods=["PUT"])
@handle_exceptions_write()
def handle_update_instructors():
    results, error_data, status_code = update_instructors(request.get_json())

    if error_data:
        return api_response_error(error_data, status_code)

    response_data, status_code = build_bulk_response(
        success_list=results,
        success_msg_single="Instructor updated successfully.",
        success_msg_bulk="{} instructors updated successfully.",
    )
    return jsonify(response_data), status_code


@instructor_bp.route("/api/instructors", methods=["PATCH"])
@handle_exceptions_write()
def handle_archive_instructors():
    payload = request.get_json()
    if not payload or "ids" not in payload:
        raise KeyError("ids")

    archived_data, error_data, status_code = archive_instructors(payload["ids"])

    if error_data:
        return api_response_error(error_data, status_code)

    response_data, status_code = build_bulk_response(
        success_list=archived_data,
        success_msg_single="Instructor archived successfully.",
        success_msg_bulk="{} instructors archived successfully.",
    )
    return jsonify(response_data), status_code
