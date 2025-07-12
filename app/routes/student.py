from flask import Blueprint, jsonify, request
from app.utils import build_bulk_response
from app.services import (
    get_all_active_students,
    get_student_by_id,
    create_students,
    update_students,
    archive_students,
)

student_bp = Blueprint("student", __name__)


@student_bp.route("/students", methods=["GET"])
def handle_read_all_active_students():
    try:
        students = get_all_active_students()
        return jsonify(
            {"message": "Students fetched successfully", "data": students}
        ), 200
    except Exception as e:
        return jsonify({"error": f"Unexpected error: {str(e)}"}), 500


@student_bp.route("/students/<int:student_id>", methods=["GET"])
def handle_get_student_by_id(student_id):
    try:
        student = get_student_by_id(student_id)

        if student is None:
            return jsonify({"error": "Student not found"}), 404

        return jsonify(
            {"message": "Student fetched successfully", "data": student}
        ), 200
    except Exception as e:
        return jsonify({"error": f"Unexpected error: {str(e)}"}), 500


@student_bp.route("/students", methods=["POST"])
def handle_create_student():
    try:
        results, error = create_students(request.get_json())

        if error:
            return error

        return build_bulk_response(
            success_list=results,
            success_msg_single="Student created successfully",
            success_msg_bulk="{} students created successfully",
            created=True,
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
        results, error = update_students(request.get_json())

        if error:
            return error

        return build_bulk_response(
            success_list=results,
            success_msg_single="Student updated successfully",
            success_msg_bulk="{} students updated successfully",
        )

    except KeyError as e:
        return jsonify({"error": f"Missing required field: {str(e)}"}), 400
    except Exception as e:
        return jsonify(
            {"error": f"Internal error while updating students: {str(e)}"}
        ), 500


@student_bp.route("/students", methods=["PATCH"])
def handle_archive_students():
    try:
        archived_ids = archive_students(request.get_json())

        if not archived_ids:
            return jsonify({"error": "No students were archived"}), 404

        return jsonify(
            {
                "message": f"{len(archived_ids)} student(s) archived successfully",
                "archived_ids": archived_ids,
            }
        ), 200

    except Exception as e:
        return jsonify(
            {"error": f"Internal error while archiving students: {str(e)}"}
        ), 500
