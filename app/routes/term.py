from flask import Blueprint, jsonify, request
from app.utils import handle_exceptions_read, handle_exceptions_write
from app.utils import build_bulk_response, api_response, api_response_error
from app.services import (
    get_all_terms,
    get_term_by_id,
    create_new_terms,
    update_terms,
    archive_terms,
)

term_bp = Blueprint("term", __name__)


@term_bp.route("/terms", methods=["GET"])
@handle_exceptions_read()
def handle_read_all_terms():
    active_only = request.args.get("active_only", "false").lower() == "true"
    terms = get_all_terms(active_only=active_only)
    return api_response(terms, "Terms fetched successfully.")


@term_bp.route("/terms/<int:term_id>", methods=["GET"])
@handle_exceptions_read()
def handle_get_term_by_id(term_id):
    term = get_term_by_id(term_id)
    if term is None:
        return api_response_error("Term not found.", 404)
    return api_response(term, "Term fetched successfully.")


@term_bp.route("/terms", methods=["POST"])
@handle_exceptions_write()
def handle_create_term():
    results, error_data, status_code = create_new_terms(request.get_json())

    if error_data:
        return api_response_error(error_data, status_code)

    response_data, status_code = build_bulk_response(
        success_list=results,
        success_msg_single="Term created successfully.",
        success_msg_bulk="{} terms created successfully.",
        created=True,
    )
    return jsonify(response_data), status_code


@term_bp.route("/terms", methods=["PUT"])
@handle_exceptions_write()
def handle_update_terms():
    results, error_data, status_code = update_terms(request.get_json())

    if error_data:
        return api_response_error(error_data, status_code)

    response_data, status_code = build_bulk_response(
        success_list=results,
        success_msg_single="Term updated successfully.",
        success_msg_bulk="{} terms updated successfully.",
    )
    return jsonify(response_data), status_code


@term_bp.route("/terms", methods=["PATCH"])
@handle_exceptions_write()
def handle_archive_terms():
    results, error_data, status_code = archive_terms(request.get_json())

    if error_data:
        return api_response_error(error_data, status_code)

    response_data, status_code = build_bulk_response(
        success_list=results,
        success_msg_single="Term archived successfully.",
        success_msg_bulk="{} terms archived successfully.",
    )
    return jsonify(response_data), status_code
