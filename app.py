import os
from flask import Flask, jsonify
from dotenv import load_dotenv
from db.database import Database

load_dotenv()

app = Flask(__name__)

app.config["ENV"] = os.getenv("FLASK_ENV", "production")
app.config["DEBUG"] = app.config["ENV"] == "development"

db = Database()

@app.route("/")
def index():
    return "Hello, the Flask API is running!"

@app.route("/students", methods=["GET"])
def get_all_students():
    query = "SELECT * FROM students WHERE status = 'active';"
    results = db.execute_query(query)  
    
    if results is None:
        return jsonify({"error": "Failed to fetch students"}), 500
    
    students = []
    for student in results:
        student_dict = {
            "id": student[0],
            "first_name": student[1],
            "last_name": student[2],
            "email": student[3],
            "address": student[4],
            "province": student[5],
            "country": student[6],
            "address_type": student[7],
            "status": student[8],
            "coop": student[9],
            "is_international": student[10],
            "program_id": student[11],
            "created_at": student[12],
            "updated_at": student[13],
            "is_archived": student[14]
        }
        students.append(student_dict)
    return jsonify(students), 200


if __name__ == "__main__":
    app.run(debug=app.config["DEBUG"], host="0.0.0.0", port=5000)
