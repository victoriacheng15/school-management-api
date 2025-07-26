import logging
from flask import Blueprint, jsonify, request
from app.utils import build_bulk_response, api_response, api_response_error
from app.services import (
    get_all_students,
    get_student_by_id,
    create_new_students,
    update_students,
    archive_students,
)

student_bp = Blueprint("student", __name__)


@student_bp.route("/students", methods=["GET"])
def handle_read_all_students():
    try:
        active_only = request.args.get("active_only", "false").lower() == "true"
        students = get_all_students(active_only=active_only)
        return api_response(students, "Students fetched successfully.")
    except Exception as e:
        logging.error(f"Student operation failed: {str(e)}.", exc_info=True)
        return api_response_error(f"Unexpected error: {str(e)}.")


@student_bp.route("/students/<int:student_id>", methods=["GET"])
def handle_get_student_by_id(student_id):
    try:
        student = get_student_by_id(student_id)

        if student is None:
            return api_response_error("Student not found.", 404)

        return api_response(student, "Student fetched successfully.")
    except Exception as e:
        return api_response_error(f"Unexpected error: {str(e)}.")


@student_bp.route("/students", methods=["POST"])
def handle_create_student():
    try:
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

    except KeyError as e:
        return api_response_error(f"Missing required field: {str(e)}.", 400)
    except Exception as e:
        logging.exception("Unexpected error during create.")
        return api_response_error(
            f"An internal error occurred while inserting the student(s): {str(e)}."
        )


@student_bp.route("/students", methods=["PUT"])
def handle_update_students():
    try:
        results, error_data, status_code = update_students(request.get_json())

        if error_data:
            return api_response_error(error_data, status_code)

        response_data, status_code = build_bulk_response(
            success_list=results,
            success_msg_single="Student updated successfully.",
            success_msg_bulk="{} students updated successfully.",
        )
        return jsonify(response_data), status_code

    except KeyError as e:
        return api_response_error(f"Missing required field: {str(e)}.", 400)
    except Exception as e:
        logging.exception("Unexpected error during update")
        return api_response_error(f"Internal error while updating students: {str(e)}.")


@student_bp.route("/students", methods=["PATCH"])
def handle_archive_students():
    try:
        payload = request.get_json()
        if not payload or "ids" not in payload:
            raise KeyError("ids")

        archived_data, error_data, status_code = archive_students(payload["ids"])

        if error_data:
            return jsonify({"errors": error_data}), status_code

        response_data, status_code = build_bulk_response(
            success_list=archived_data,
            success_msg_single="Student archived successfully.",
            success_msg_bulk="{} students archived successfully.",
        )
        return jsonify(response_data), status_code

    except KeyError as e:
        return api_response_error(f"Missing required field: {str(e)}.", 400)
    except Exception as e:
        logging.exception("Unexpected error during archive.")
        return api_response_error(f"Internal error while archiving students: {str(e)}.")
