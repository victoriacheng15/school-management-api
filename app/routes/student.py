from flask import Blueprint, jsonify, request
from app.models import (
    read_all_active_students,
    create_student,
    read_student_by_id,
    update_student,
    archive_student,
)
from app.utils import (
    student_row_to_dict,
    student_dict_to_row,
    handle_bulk_process,
    build_bulk_response,
    normalize_to_list,
)

student_bp = Blueprint("student", __name__)


@student_bp.route("/students", methods=["GET"])
def handle_read_all_active_students():
    try:
        results = read_all_active_students()

        if results is None:
            return jsonify({"error": "Failed to fetch students"}), 500

        students = [student_row_to_dict(student) for student in results]
        return jsonify({
            "message": "Students fetched successfully",
            "data": students
        }), 200
    except Exception as e:
        return jsonify({"error": f"Unexpected error: {str(e)}"}), 500


@student_bp.route("/students/<int:student_id>", methods=["GET"])
def handle_get_student_by_id(student_id):
    try:
        student = read_student_by_id(student_id)

        if student is None:
            return jsonify({"error": "Student not found"}), 404
        
        return jsonify({
            "message": "Student fetched successfully",
            "data": student_row_to_dict(student)
        }), 200
    except Exception as e:
        return jsonify({"error": f"Unexpected error: {str(e)}"}), 500


@student_bp.route("/students", methods=["POST"])
def handle_create_student():
    try:
        data = normalize_to_list(request.get_json())
        results, error = handle_bulk_process(
            items=data,
            process_func=create_student,
            success_func=read_student_by_id,
            dict_to_row_func=student_dict_to_row,
            row_to_dict_func=student_row_to_dict
        )

        if error:
            return error
        
        return build_bulk_response(
            success_list=results,
            success_msg_single="Student created successfully",
            success_msg_bulk="{} students created successfully",
            created=True
        )

    except KeyError as e:
        return jsonify({"error": f"Missing required field: {str(e)}"}), 400
    except Exception as e:
        return jsonify(
            {"error": f"An internal error occurred while inserting the student(s)."}
        ), 500

@student_bp.route("/students", methods=["PUT"])
def handle_update_students():
    try:
        data = normalize_to_list(request.get_json())
        results, error = handle_bulk_process(
            items=data,
            process_func=update_student,
            success_func=read_student_by_id,
            id_key="id",
            missing_id_msg="Missing 'id' field in student update data",
            dict_to_row_func=student_dict_to_row,
            row_to_dict_func=student_row_to_dict
        )
        if error:
            return error

        return build_bulk_response(
            success_list=results,
            success_msg_single="Student updated successfully",
            success_msg_bulk="{} students updated successfully"
        )

    except KeyError as e:
        return jsonify({"error": f"Missing required field: {str(e)}"}), 400
    except Exception as e:
        return jsonify({"error": f"Internal error while updating students: {str(e)}"}), 500


@student_bp.route("/students", methods=["PATCH"])
def handle_archive_students():
    try:
        ids = normalize_to_list(request.get_json())

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
