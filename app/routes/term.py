from flask import Blueprint, jsonify
from app.models import get_all_active_terms
from app.utils import term_row_to_dict

term_bp = Blueprint("term", __name__)


@term_bp.route("/terms", methods=["GET"])
def handle_get_all_terms():
    results = get_all_active_terms()
    if results is None:
        return jsonify({"error": "Failed to fetch terms"}), 500
    terms = [term_row_to_dict(row) for row in results]
    return jsonify(terms), 200
