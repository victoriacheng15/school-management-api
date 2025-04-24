from flask import Blueprint, jsonify
from models.student_model import get_all_active_students
from utils.converters import student_row_to_dict

student_bp = Blueprint("student", __name__)

@student_bp.route("/students", methods=["GET"])
def get_all_students():
    results = get_all_active_students()

    if results is None:
        return jsonify({"error": "Failed to fetch students"}), 500
    
    students = [student_row_to_dict(student) for student in results] 
    return jsonify(students), 200