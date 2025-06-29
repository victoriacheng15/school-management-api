from flask import Blueprint, jsonify
from models.enrollment import get_all_enrollments
from utils.converters import enrollment_row_to_dict

enrollment_bp = Blueprint("enrollment", __name__)

@enrollment_bp.route("/enrollments", methods=["GET"])
def handle_get_all_enrollments():
    results = get_all_enrollments()
    if results is None:
        return jsonify({"error": "Failed to fetch enrollments"}), 500
    enrollments = [enrollment_row_to_dict(row) for row in results]
    return jsonify(enrollments), 200