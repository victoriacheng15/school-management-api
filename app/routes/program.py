from flask import Blueprint, jsonify, request
from app.utils import (
    build_bulk_response,
    api_response,
    api_response_error,
    handle_exceptions_read,
    handle_exceptions_write,
)
from app.services import (
    get_all_programs,
    get_program_by_id,
    create_new_programs,
    update_programs,
    archive_programs,
)

program_bp = Blueprint("program", __name__)


@program_bp.route("/api/programs", methods=["GET"])
@handle_exceptions_read()
def handle_read_all_programs():
    active_only = request.args.get("active_only", "false").lower() == "true"
    programs = get_all_programs(active_only=active_only)
    return api_response(programs, "Programs fetched successfully.")


@program_bp.route("/api/programs/<int:program_id>", methods=["GET"])
@handle_exceptions_read()
def handle_get_program_by_id(program_id):
    program = get_program_by_id(program_id)
    if program is None:
        return api_response_error("Program not found.", 404)
    return api_response(program, "Program fetched successfully.")


@program_bp.route("/api/programs", methods=["POST"])
@handle_exceptions_write()
def handle_create_program():
    results, error_data, status_code = create_new_programs(request.get_json())

    if error_data:
        return api_response_error(error_data, status_code)

    response_data, status_code = build_bulk_response(
        success_list=results,
        success_msg_single="Program created successfully.",
        success_msg_bulk="{} programs created successfully.",
        created=True,
    )
    return jsonify(response_data), status_code


@program_bp.route("/api/programs", methods=["PUT"])
@handle_exceptions_write()
def handle_update_programs():
    results, error_data, status_code = update_programs(request.get_json())

    if error_data:
        return api_response_error(error_data, status_code)

    response_data, status_code = build_bulk_response(
        success_list=results,
        success_msg_single="Program updated successfully.",
        success_msg_bulk="{} programs updated successfully.",
    )
    return jsonify(response_data), status_code


@program_bp.route("/api/programs", methods=["PATCH"])
@handle_exceptions_write()
def handle_archive_programs():
    payload = request.get_json()
    if not payload or "ids" not in payload:
        raise KeyError("ids")

    archived_data, error_data, status_code = archive_programs(payload["ids"])

    if error_data:
        return api_response_error(error_data, status_code)

    response_data, status_code = build_bulk_response(
        success_list=archived_data,
        success_msg_single="Program archived successfully.",
        success_msg_bulk="{} programs archived successfully.",
    )
    return jsonify(response_data), status_code
