import os
from flask import Flask
from dotenv import load_dotenv

load_dotenv()


def create_app():
    app = Flask(__name__)

    app.config["ENV"] = os.getenv("FLASK_ENV", "production")
    app.config["DEBUG"] = app.config["ENV"] == "development"

    # Import and register blueprints
    from app.routes.home import home_bp
    from app.routes.assignment import assignment_bp
    from app.routes.course import course_bp
    from app.routes.course_schedule import course_schedule_bp
    from app.routes.department import department_bp
    from app.routes.enrollment import enrollment_bp
    from app.routes.instructor import instructor_bp
    from app.routes.program import program_bp
    from app.routes.student import student_bp
    from app.routes.term import term_bp

    app.register_blueprint(home_bp)
    app.register_blueprint(assignment_bp)
    app.register_blueprint(course_bp)
    app.register_blueprint(course_schedule_bp)
    app.register_blueprint(department_bp)
    app.register_blueprint(enrollment_bp)
    app.register_blueprint(instructor_bp)
    app.register_blueprint(program_bp)
    app.register_blueprint(student_bp)
    app.register_blueprint(term_bp)

    return app
