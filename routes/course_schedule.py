from flask import Blueprint, jsonify
from models.course_schedule import get_all_active_course_schedules
from utils.converters import course_schedule_row_to_dict

course_schedule_bp = Blueprint("course_schedule", __name__)

@course_schedule_bp.route("/course_schedule", methods=["GET"])
def get_all_course_schedule():
    results = get_all_active_course_schedules()
    if results is None:
        return jsonify({"error": "Failed to fetch course schedule"}), 500
    schedules = [course_schedule_row_to_dict(row) for row in results]
    return jsonify(schedules), 200