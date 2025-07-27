import os
from flask import Flask
from dotenv import load_dotenv

load_dotenv()


def create_app():
    app = Flask(__name__)

    app.config["ENV"] = os.getenv("FLASK_ENV", "production")
    app.config["DEBUG"] = app.config["ENV"] == "development"

    # Import and register blueprints
    from app.routes import home_bp
    from app.routes import assignment_bp
    from app.routes import course_bp
    from app.routes import course_schedule_bp
    from app.routes import department_bp
    from app.routes import enrollment_bp
    from app.routes import instructor_bp
    from app.routes import program_bp
    from app.routes import student_bp
    from app.routes import term_bp
    from app.routes import enrollment_bp
    from app.routes import course_schedule_bp

    blueprints = [
        home_bp,
        assignment_bp,
        course_bp,
        course_schedule_bp,
        department_bp,
        enrollment_bp,
        instructor_bp,
        program_bp,
        student_bp,
        term_bp,
    ]
    for blueprint in blueprints:
        app.register_blueprint(blueprint)

    return app
