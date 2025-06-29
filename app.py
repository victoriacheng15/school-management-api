import os
from flask import Flask
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

app.config["ENV"] = os.getenv("FLASK_ENV", "production")
app.config["DEBUG"] = app.config["ENV"] == "development"

from routes.home import home_bp
from routes.assignment import assignment_bp
from routes.course import course_bp
from routes.course_schedule import course_schedule_bp
from routes.department import department_bp
from routes.enrollment import enrollment_bp
from routes.instructor import instructor_bp
from routes.program import program_bp
from routes.student import student_bp
from routes.term import term_bp

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


if __name__ == "__main__":
    app.run(debug=app.config["DEBUG"], host="0.0.0.0", port=5000)
