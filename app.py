from flask import Flask
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)

app.config["ENV"] = os.getenv("FLASK_ENV", "production")
app.config["DEBUG"] = app.config["ENV"] == "development"


@app.route("/")
def index():
    return "Hello, the Flask API is running!"


if __name__ == "__main__":
    app.run(debug=app.config["DEBUG"], host="0.0.0.0", port=5000)
