from flask import Blueprint, jsonify

home_bp = Blueprint("home", __name__)


@home_bp.route("/")
def index():
    return jsonify(
        {
            "message": "Welcome to the Student API",
            "status": "OK",
            "version": "1.0",
            "available_routes": [
                "/assignments",
                "/course_schedule",
                "/courses",
                "/departments",
                "/enrollments",
                "/instructors",
                "/programs",
                "/students",
                "/terms",
            ],
        }
    ), 200
