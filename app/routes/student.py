from flask import Blueprint, jsonify, request
from app.models import (
    read_all_active_students,
    create_student,
    read_student_by_id,
    update_student,
    archive_student,
)
from app.utils import student_row_to_dict, student_dict_to_row

student_bp = Blueprint("student", __name__)


@student_bp.route("/students", methods=["GET"])
def handle_read_all_active_students():
    try:
        results = read_all_active_students()

        if results is None:
            return jsonify({"error": "Failed to fetch students"}), 500

        students = [student_row_to_dict(student) for student in results]
        return jsonify(students), 200
    except Exception as e:
        return jsonify({"error": f"Unexpected error: {str(e)}"}), 500


@student_bp.route("/students/<int:student_id>", methods=["GET"])
def handle_get_student_by_id(student_id):
    try:
        student = read_student_by_id(student_id)

        if student is None:
            return jsonify({"error": "Student not found"}), 404
        
        return jsonify(student_row_to_dict(student)), 200
    except Exception as e:
        return jsonify({"error": f"Unexpected error: {str(e)}"}), 500


@student_bp.route("/students", methods=["POST"])
def handle_create_student():
    try:
        data = request.get_json()
        students = data if isinstance(data, list) else [data]
        created_students = []

        for item in students:
            row = student_dict_to_row(item)
            inserted_id = create_student(row)
            student = read_student_by_id(inserted_id)
            if student:
                created_students.append(student_row_to_dict(student))

        if not created_students:
            return jsonify({"error": "Failed to insert student(s)"}), 500

        if len(created_students) == 1:
            return jsonify(
                {
                    "message": "Student created successfully",
                    "data": created_students[0],
                }
            ), 201
        else:
            return jsonify(
                {
                    "message": f"{len(created_students)} students created successfully",
                    "data": created_students,
                }
            ), 201

    except KeyError as e:
        return jsonify({"error": f"Missing required field: {str(e)}"}), 400
    except Exception as e:
        return jsonify(
            {"error": f"An internal error occurred while inserting the student(s)."}
        ), 500

@student_bp.route("/students", methods=["PUT"])
def handle_update_students():
    try:
        data = request.get_json()
        students = data if isinstance(data, list) else [data]
        updated_students = []

        for student_data in students:
            student_id = student_data.get("id")
            if not student_id:
                return jsonify({"error": "Missing 'id' field in student update data"}), 400

            row = student_dict_to_row(student_data)
            rows_updated = update_student(student_id, row)

            if rows_updated > 0:
                student = read_student_by_id(student_id)
                if student:
                    updated_students.append(student_row_to_dict(student))

        if not updated_students:
            return jsonify({"error": "No student records updated"}), 404

        if len(updated_students) == 1:
            return jsonify({
                "message": "Student updated successfully",
                "data": updated_students[0]
            }), 200
        else:
            return jsonify({
                "message": f"{len(updated_students)} students updated successfully",
                "data": updated_students
            }), 200

    except KeyError as e:
        return jsonify({"error": f"Missing required field: {str(e)}"}), 400
    except Exception as e:
        return jsonify({"error": f"Internal error while updating students: {str(e)}"}), 500


@student_bp.route("/students", methods=["PATCH"])
def handle_archive_students():
    try:
        data = request.get_json()
        ids = data if isinstance(data, list) else [data]

        if not all(isinstance(item, int) for item in ids):
            return jsonify({"error": "Input must be an integer or list of integers (student IDs)"}), 400

        archived_ids = []
        for student_id in ids:
            rows_updated = archive_student(student_id)
            if rows_updated > 0:
                archived_ids.append(student_id)

        if not archived_ids:
            return jsonify({"error": "No students were archived"}), 404

        return jsonify({
            "message": f"{len(archived_ids)} student(s) archived successfully",
            "archived_ids": archived_ids
        }), 200

    except Exception as e:
        return jsonify({"error": f"Internal error while archiving students: {str(e)}"}), 500
