import logging
from flask import Blueprint, jsonify, request
from app.utils import build_bulk_response, api_response, api_response_error
from app.services import (
    get_all_courses,
    get_course_by_id,
    create_new_courses,
    update_courses,
    archive_courses,
)

course_bp = Blueprint("course", __name__)


@course_bp.route("/courses", methods=["GET"])
def handle_read_all_courses():
    try:
        active_only = request.args.get("active_only", "false").lower() == "true"
        courses = get_all_courses(active_only=active_only)
        return api_response(courses, "Courses fetched successfully.")
    except Exception as e:
        logging.error(f"Course operation failed: {str(e)}.", exc_info=True)
        return api_response_error(f"Unexpected error: {str(e)}.")


@course_bp.route("/courses/<int:course_id>", methods=["GET"])
def handle_get_course_by_id(course_id):
    try:
        course = get_course_by_id(course_id)

        if course is None:
            return api_response_error("Course not found.", 404)

        return api_response(course, "Course fetched successfully.")
    except Exception as e:
        return api_response_error(f"Unexpected error: {str(e)}.")


@course_bp.route("/courses", methods=["POST"])
def handle_create_course():
    try:
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

    except KeyError as e:
        return api_response_error(f"Missing required field: {str(e)}.", 400)
    except Exception as e:
        logging.exception("Unexpected error during create.")
        return api_response_error(
            f"An internal error occurred while inserting the course(s): {str(e)}."
        )


@course_bp.route("/courses", methods=["PUT"])
def handle_update_courses():
    try:
        results, error_data, status_code = update_courses(request.get_json())

        if error_data:
            return api_response_error(error_data, status_code)

        response_data, status_code = build_bulk_response(
            success_list=results,
            success_msg_single="Course updated successfully.",
            success_msg_bulk="{} courses updated successfully.",
        )
        return jsonify(response_data), status_code

    except KeyError as e:
        return api_response_error(f"Missing required field: {str(e)}.", 400)
    except Exception as e:
        logging.exception("Unexpected error during update")
        return api_response_error(f"Internal error while updating courses: {str(e)}.")


@course_bp.route("/courses", methods=["PATCH"])
def handle_archive_courses():
    try:
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

    except KeyError as e:
        return api_response_error(f"Missing required field: {str(e)}.", 400)
    except Exception as e:
        logging.exception("Unexpected error during archive.")
        return api_response_error(f"Internal error while archiving courses: {str(e)}.")