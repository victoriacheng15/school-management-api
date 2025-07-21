from flask import Blueprint, jsonify, request
from app.utils import build_bulk_response, api_response, api_response_error
from app.services import (
    get_all_instructors,
    get_instructor_by_id,
    create_new_instructors,
    update_instructors,
    archive_instructors,
)

instructor_bp = Blueprint("instructor", __name__)


@instructor_bp.route("/instructors", methods=["GET"])
def handle_read_all_instructors():
    try:
        instructors = get_all_instructors()
        return api_response(instructors, "Instructors fetched successfully")
    except Exception as e:
        return api_response_error(f"Unexpected error: {str(e)}")


@instructor_bp.route("/instructors/<int:instructor_id>", methods=["GET"])
def handle_get_instructor_by_id(instructor_id):
    try:
        instructor = get_instructor_by_id(instructor_id)

        if instructor is None:
            return api_response_error("Instructor not found", 404)

        return api_response(instructor, "Instructor fetched successfully")
    except Exception as e:
        return api_response_error(f"Unexpected error: {str(e)}")


@instructor_bp.route("/instructors", methods=["POST"])
def handle_create_instructor():
    try:
        results, error_data, status_code = create_new_instructors(request.get_json())

        if error_data:
            return api_response_error(error_data["error"], status_code)

        response_data, status_code = build_bulk_response(
            success_list=results,
            success_msg_single="Instructor created successfully",
            success_msg_bulk="{} instructors created successfully",
            created=True,
        )
        return jsonify(response_data), status_code

    except KeyError as e:
        return api_response_error(f"Missing required field: {str(e)}")
    except Exception as e:
        return api_response_error(
            f"An internal error occurred while inserting the instructor(s): {str(e)}"
        )


@instructor_bp.route("/instructors", methods=["PUT"])
def handle_update_instructors():
    try:
        results, error_messages, status_code = update_instructors(request.get_json())
        if error_messages:
            return api_response_error(error_messages, status_code)

        response_data, status_code = build_bulk_response(
            success_list=results,
            success_msg_single="Instructor updated successfully",
            success_msg_bulk="{} instructors updated successfully",
        )
        return jsonify(response_data), status_code

    except KeyError as e:
        return api_response_error(f"Missing required field: {str(e)}", 400)
    except Exception as e:
        return api_response_error(
            f"Internal error while updating instructors: {str(e)}"
        )


@instructor_bp.route("/instructors", methods=["PATCH"])
def handle_archive_instructors():
    try:
        payload = request.get_json()

        if not payload or "ids" not in payload:
            raise KeyError("ids")

        archived_data, error_messages, status_code = archive_instructors(payload["ids"])

        if error_messages:
            return api_response_error(error_messages, status_code)
        response_data, status_code = build_bulk_response(
            success_list=archived_data,
            success_msg_single="Instructor archived successfully",
            success_msg_bulk="{} instructors archived successfully",
        )

        return jsonify(response_data), status_code

    except KeyError as e:
        return api_response_error(f"Missing required field: {str(e)}", 400)
    except Exception as e:
        return api_response_error(
            f"Internal error while archiving instructors: {str(e)}"
        )
