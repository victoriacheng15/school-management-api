from flask import Blueprint, jsonify, request
from app.utils import (
    build_bulk_response,
    api_response,
    api_response_error,
    handle_exceptions_read,
    handle_exceptions_write,
)
from app.services import (
    get_all_course_schedules,
    get_course_schedule_by_id,
    create_new_course_schedules,
    update_course_schedules,
    archive_course_schedules,
)

course_schedule_bp = Blueprint("course_schedule", __name__)


@course_schedule_bp.route("/api/course_schedules", methods=["GET"])
@handle_exceptions_read()
def handle_read_all_course_schedules():
    active_only = request.args.get("active_only", "false").lower() == "true"
    course_schedules = get_all_course_schedules(active_only=active_only)
    return api_response(course_schedules, "Course schedules fetched successfully.")


@course_schedule_bp.route("/api/course_schedules/<int:course_schedule_id>", methods=["GET"])
@handle_exceptions_read()
def handle_get_course_schedule_by_id(course_schedule_id):
    course_schedule = get_course_schedule_by_id(course_schedule_id)
    if course_schedule is None:
        return api_response_error("Course schedule not found.", 404)
    return api_response(course_schedule, "Course schedule fetched successfully.")


@course_schedule_bp.route("/api/course_schedules", methods=["POST"])
@handle_exceptions_write()
def handle_create_course_schedule():
    results, error_data, status_code = create_new_course_schedules(request.get_json())

    if error_data:
        return api_response_error(error_data, status_code)

    response_data, status_code = build_bulk_response(
        success_list=results,
        success_msg_single="Course schedule created successfully.",
        success_msg_bulk="{} course schedules created successfully.",
        created=True,
    )
    return jsonify(response_data), status_code


@course_schedule_bp.route("/api/course_schedules", methods=["PUT"])
@handle_exceptions_write()
def handle_update_course_schedules():
    results, error_data, status_code = update_course_schedules(request.get_json())

    if error_data:
        return api_response_error(error_data, status_code)

    response_data, status_code = build_bulk_response(
        success_list=results,
        success_msg_single="Course schedule updated successfully.",
        success_msg_bulk="{} course schedules updated successfully.",
    )
    return jsonify(response_data), status_code


@course_schedule_bp.route("/api/course_schedules", methods=["PATCH"])
@handle_exceptions_write()
def handle_archive_course_schedules():
    payload = request.get_json()
    if not payload or "ids" not in payload:
        raise KeyError("ids")

    archived_data, error_data, status_code = archive_course_schedules(payload["ids"])

    if error_data:
        return api_response_error(error_data, status_code)

    response_data, status_code = build_bulk_response(
        success_list=archived_data,
        success_msg_single="Course schedule archived successfully.",
        success_msg_bulk="{} course schedules archived successfully.",
    )
    return jsonify(response_data), status_code
