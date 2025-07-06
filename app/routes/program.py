from flask import Blueprint, jsonify
from app.models.program import get_all_active_programs
from app.utils.converters import program_row_to_dict

program_bp = Blueprint("program", __name__)


@program_bp.route("/programs", methods=["GET"])
def handle_get_all_programs():
    results = get_all_active_programs()
    if results is None:
        return jsonify({"error": "Failed to fetch programs"}), 500
    programs = [program_row_to_dict(row) for row in results]
    return jsonify(programs), 200
