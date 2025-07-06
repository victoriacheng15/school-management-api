from flask import Blueprint, jsonify
from app.models import get_all_active_assignments
from app.utils import assignment_row_to_dict

assignment_bp = Blueprint("assignment", __name__)


@assignment_bp.route("/assignments", methods=["GET"])
def handle_get_all_assignments():
    results = get_all_active_assignments()
    if results is None:
        return jsonify({"error": "Failed to fetch assignments"}), 500
    assignments = [assignment_row_to_dict(row) for row in results]
    return jsonify(assignments), 200
