from flask import Blueprint, jsonify
from models.term import get_all_terms
from utils.converters import term_row_to_dict

term_bp = Blueprint("term", __name__)

@term_bp.route("/terms", methods=["GET"])
def handle_get_all_terms():
    results = get_all_terms()
    if results is None:
        return jsonify({"error": "Failed to fetch terms"}), 500
    terms = [term_row_to_dict(row) for row in results]
    return jsonify(terms), 200