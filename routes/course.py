from flask import Blueprint, jsonify
from models.course import get_all_active_courses
from utils.converters import course_row_to_dict

course_bp = Blueprint("course", __name__)

@course_bp.route("/courses", methods=["GET"])
def handle_get_all_courses():
    results = get_all_active_courses()
    if results is None:
        return jsonify({"error": "Failed to fetch courses"}), 500
    courses = [course_row_to_dict(row) for row in results]
    return jsonify(courses), 200