import os
from flask import Flask
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

app.config["ENV"] = os.getenv("FLASK_ENV", "production")
app.config["DEBUG"] = app.config["ENV"] == "development"

from routes.home_route import home_bp
from routes.student_route import student_bp

app.register_blueprint(home_bp)
app.register_blueprint(student_bp)


if __name__ == "__main__":
    app.run(debug=app.config["DEBUG"], host="0.0.0.0", port=5000)
