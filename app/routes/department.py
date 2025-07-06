from flask import Blueprint, jsonify
from app.models import get_all_active_departments
from app.utils import department_row_to_dict

department_bp = Blueprint("department", __name__)


@department_bp.route("/departments", methods=["GET"])
def handle_get_all_departments():
    results = get_all_active_departments()
    if results is None:
        return jsonify({"error": "Failed to fetch departments"}), 500
    departments = [department_row_to_dict(row) for row in results]
    return jsonify(departments), 200
