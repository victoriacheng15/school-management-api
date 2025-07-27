import logging
from flask import Blueprint, jsonify, request
from app.utils import handle_exceptions_read, handle_exceptions_write
from app.utils import build_bulk_response, api_response, api_response_error
from app.services import (
    get_all_assignments,
    get_assignment_by_id,
    create_new_assignments,
    update_assignments,
    archive_assignments,
)

assignment_bp = Blueprint("assignment", __name__)


@assignment_bp.route("/assignments", methods=["GET"])
@handle_exceptions_read()
def handle_read_all_assignments():
    active_only = request.args.get("active_only", "false").lower() == "true"
    assignments = get_all_assignments(active_only=active_only)
    return api_response(assignments, "Assignments fetched successfully.")


@assignment_bp.route("/assignments/<int:assignment_id>", methods=["GET"])
@handle_exceptions_read()
def handle_get_assignment_by_id(assignment_id):
    assignment = get_assignment_by_id(assignment_id)
    if assignment is None:
        return api_response_error("Assignment not found.", 404)
    return api_response(assignment, "Assignment fetched successfully.")


@assignment_bp.route("/assignments", methods=["POST"])
@handle_exceptions_write()
def handle_create_assignment():
    results, error_data, status_code = create_new_assignments(request.get_json())

    if error_data:
        return api_response_error(error_data, status_code)

    response_data, status_code = build_bulk_response(
        success_list=results,
        success_msg_single="Assignment created successfully.",
        success_msg_bulk="{} assignments created successfully.",
        created=True,
    )
    return jsonify(response_data), status_code


@assignment_bp.route("/assignments", methods=["PUT"])
@handle_exceptions_write()
def handle_update_assignments():
    results, error_data, status_code = update_assignments(request.get_json())

    if error_data:
        return api_response_error(error_data, status_code)

    response_data, status_code = build_bulk_response(
        success_list=results,
        success_msg_single="Assignment updated successfully.",
        success_msg_bulk="{} assignments updated successfully.",
    )
    return jsonify(response_data), status_code


@assignment_bp.route("/assignments", methods=["PATCH"])
@handle_exceptions_write()
def handle_archive_assignments():
    payload = request.get_json()
    if not payload or "ids" not in payload:
        raise KeyError("ids")

    archived_data, error_data, status_code = archive_assignments(payload["ids"])

    if error_data:
        return api_response_error(error_data, status_code)

    response_data, status_code = build_bulk_response(
        success_list=archived_data,
        success_msg_single="Assignment archived successfully.",
        success_msg_bulk="{} assignments archived successfully.",
    )
    return jsonify(response_data), status_code
