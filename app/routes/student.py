from flask import Blueprint, jsonify, request
from app.models.student import (
    get_all_active_students,
    insert_student,
    get_student_by_id,
)
from app.utils.converters import student_row_to_dict, student_dict_to_row

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


@student_bp.route("/students/<int:student_id>", methods=["GET"])
def handle_get_student_by_id(student_id):
    try:
        student = get_student_by_id(student_id)
        if student is None:
            return jsonify({"error": "Student not found"}), 404
        return jsonify(student_row_to_dict(student)), 200
    except Exception as e:
        return jsonify({"error": f"Unexpected error: {str(e)}"}), 500


@student_bp.route("/students", methods=["POST"])
def handle_insert_student():
    try:
        data = request.get_json()
        # Always work with a list for simplicity
        students = data if isinstance(data, list) else [data]
        inserted_students = []

        for item in students:
            row = student_dict_to_row(item)
            inserted_id = insert_student(row)
            student = get_student_by_id(inserted_id)
            if student:
                inserted_students.append(student_row_to_dict(student))

        if not inserted_students:
            return jsonify({"error": "Failed to insert student(s)"}), 500

        # Return single object if only one inserted, else list
        if len(inserted_students) == 1:
            return jsonify(
                {
                    "message": "Student inserted successfully",
                    "data": inserted_students[0],
                }
            ), 201
        else:
            return jsonify(
                {
                    "message": f"{len(inserted_students)} students inserted successfully",
                    "data": inserted_students,
                }
            ), 201

    except KeyError as e:
        return jsonify({"error": f"Missing required field: {str(e)}"}), 400
    except Exception as e:
        return jsonify(
            {"error": f"An internal error occurred while inserting the student(s)."}
        ), 500
