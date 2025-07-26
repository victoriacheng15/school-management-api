import logging
from flask import Blueprint, jsonify, request
from app.utils import build_bulk_response, api_response, api_response_error
from app.services import (
    get_all_departments,
    get_department_by_id,
    create_new_departments,
    update_departments,
    archive_departments,
)

department_bp = Blueprint("department", __name__)


@department_bp.route("/departments", methods=["GET"])
def handle_read_all_departments():
    try:
        active_only = request.args.get("active_only", "false").lower() == "true"
        departments = get_all_departments(active_only=active_only)
        return api_response(departments, "Departments fetched successfully.")
    except Exception as e:
        logging.error(f"Department operation failed: {str(e)}.", exc_info=True)
        return api_response_error(f"Unexpected error: {str(e)}.")


@department_bp.route("/departments/<int:department_id>", methods=["GET"])
def handle_get_department_by_id(department_id):
    try:
        department = get_department_by_id(department_id)

        if department is None:
            return api_response_error("Department not found.", 404)

        return api_response(department, "Department fetched successfully.")
    except Exception as e:
        return api_response_error(f"Unexpected error: {str(e)}.")


@department_bp.route("/departments", methods=["POST"])
def handle_create_department():
    try:
        results, error_data, status_code = create_new_departments(request.get_json())

        if error_data:
            return api_response_error(error_data, status_code)

        response_data, status_code = build_bulk_response(
            success_list=results,
            success_msg_single="Department created successfully.",
            success_msg_bulk="{} departments created successfully.",
            created=True,
        )
        return jsonify(response_data), status_code

    except KeyError as e:
        return api_response_error(f"Missing required field: {str(e)}.", 400)
    except Exception as e:
        logging.exception("Unexpected error during create.")
        return api_response_error(
            f"An internal error occurred while inserting the department(s): {str(e)}."
        )


@department_bp.route("/departments", methods=["PUT"])
def handle_update_departments():
    try:
        results, error_data, status_code = update_departments(request.get_json())

        if error_data:
            return api_response_error(error_data, status_code)

        response_data, status_code = build_bulk_response(
            success_list=results,
            success_msg_single="Department updated successfully.",
            success_msg_bulk="{} departments updated successfully.",
        )
        return jsonify(response_data), status_code

    except KeyError as e:
        return api_response_error(f"Missing required field: {str(e)}.", 400)
    except Exception as e:
        logging.exception("Unexpected error during update.")
        return api_response_error(
            f"Internal error while updating departments: {str(e)}."
        )


@department_bp.route("/departments", methods=["PATCH"])
def handle_archive_departments():
    try:
        payload = request.get_json()
        if not payload or "ids" not in payload:
            raise KeyError("ids")

        archived_data, error_data, status_code = archive_departments(payload["ids"])

        if error_data:
            return api_response_error(error_data, status_code)

        response_data, status_code = build_bulk_response(
            success_list=archived_data,
            success_msg_single="Department archived successfully.",
            success_msg_bulk="{} departments archived successfully.",
        )

        return jsonify(response_data), status_code

    except KeyError as e:
        return api_response_error(f"Missing required field: {str(e)}", 400)
    except Exception as e:
        logging.exception("Unexpected error during archive.")
        return api_response_error(
            f"Internal error while archiving departments: {str(e)}."
        )
