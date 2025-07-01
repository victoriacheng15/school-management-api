from flask import Blueprint, jsonify, request
from models.student import get_all_active_students, insert_student, get_student_by_id
from utils.converters import student_row_to_dict, student_dict_to_row

student_bp = Blueprint("student", __name__)

@student_bp.route("/students", methods=["GET"])
def handle_get_all_students():
    try:
        results = get_all_active_students()

        if results is None:
            return jsonify({"error": "Failed to fetch students"}), 500
    
        students = [student_row_to_dict(student) for student in results] 
        return jsonify(students), 200
    except Exception as e:
        return jsonify({"error": f"Unexpected error: {str(e)}"}), 500

@student_bp.route("/students", methods=["POST"])
def handle_insert_student():
    try:
        data = request.get_json()
        row = student_dict_to_row(data)
        inserted_id = insert_student(row)
        student = get_student_by_id(inserted_id)

        if student is None:
            return jsonify({"error": "Failed to insert student"}), 500
        return jsonify({"message": "Student inserted successfully", "data": student_row_to_dict(student)}), 201

    except KeyError as e:
        return jsonify({"error": f"Missing required field: {str(e)}"}), 400
    except Exception as e:
        return jsonify({"error": f"An internal error occurred while inserting the student."}), 500