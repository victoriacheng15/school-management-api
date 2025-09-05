from flask import Blueprint, jsonify, request
from app.utils import (
    build_bulk_response,
    api_response,
    api_response_error,
    handle_exceptions_read,
    handle_exceptions_write,
)
from app.services import (
    get_all_enrollments,
    get_enrollment_by_id,
    create_new_enrollments,
    update_enrollments,
    archive_enrollments,
)

enrollment_bp = Blueprint("enrollment", __name__)


@enrollment_bp.route("/enrollments", methods=["GET"])
@handle_exceptions_read()
def handle_read_all_enrollments():
    active_only = request.args.get("active_only", "false").lower() == "true"
    enrollments = get_all_enrollments(active_only=active_only)
    return api_response(enrollments, "Enrollments fetched successfully.")


@enrollment_bp.route("/enrollments/<int:enrollment_id>", methods=["GET"])
@handle_exceptions_read()
def handle_get_enrollment_by_id(enrollment_id):
    enrollment = get_enrollment_by_id(enrollment_id)
    if enrollment is None:
        return api_response_error("Enrollment not found.", 404)
    return api_response(enrollment, "Enrollment fetched successfully.")


@enrollment_bp.route("/enrollments", methods=["POST"])
@handle_exceptions_write()
def handle_create_enrollment():
    results, error_data, status_code = create_new_enrollments(request.get_json())

    if error_data:
        return api_response_error(error_data, status_code)

    response_data, status_code = build_bulk_response(
        success_list=results,
        success_msg_single="Enrollment created successfully.",
        success_msg_bulk="{} enrollments created successfully.",
        created=True,
    )
    return jsonify(response_data), status_code


@enrollment_bp.route("/enrollments", methods=["PUT"])
@handle_exceptions_write()
def handle_update_enrollments():
    results, error_data, status_code = update_enrollments(request.get_json())

    if error_data:
        return api_response_error(error_data, status_code)

    response_data, status_code = build_bulk_response(
        success_list=results,
        success_msg_single="Enrollment updated successfully.",
        success_msg_bulk="{} enrollments updated successfully.",
    )
    return jsonify(response_data), status_code


@enrollment_bp.route("/enrollments", methods=["PATCH"])
@handle_exceptions_write()
def handle_archive_enrollments():
    ids = request.get_json().get("ids", [])
    results, error_data, status_code = archive_enrollments(ids)

    if error_data:
        return api_response_error(error_data, status_code)

    response_data, status_code = build_bulk_response(
        success_list=results,
        success_msg_single="Enrollment archived successfully.",
        success_msg_bulk="{} enrollments archived successfully.",
    )
    return jsonify(response_data), status_code
