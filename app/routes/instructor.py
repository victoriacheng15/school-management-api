from flask import Blueprint, jsonify
from app.models.instructor import get_all_active_instructors
from app.utils.converters import instructor_row_to_dict

instructor_bp = Blueprint("instructor", __name__)

@instructor_bp.route("/instructors", methods=["GET"])
def handle_get_all_instructors():
    results = get_all_active_instructors()
    if results is None:
        return jsonify({"error": "Failed to fetch instructors"}), 500
    instructors = [instructor_row_to_dict(row) for row in results]
    return jsonify(instructors), 200