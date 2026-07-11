from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)

FRONTEND = os.path.join(os.path.dirname(__file__), "..", "Frontend")

history = []

@app.route("/")
def home():
    return send_from_directory(FRONTEND, "login.html")

@app.route("/login")
def login():
    return send_from_directory(FRONTEND, "login.html")
    
@app.route("/register")
def register():
    return send_from_directory(FRONTEND, "register.html")

@app.route("/dashboard")
def dashboard():
    return send_from_directory(FRONTEND, "dashboard.html")

@app.route("/prediction")
def prediction():
    return send_from_directory(FRONTEND, "prediction.html")

@app.route("/history")
def history_page():
    return send_from_directory(FRONTEND, "history.html")

@app.route("/profile")
def profile():
    return send_from_directory(FRONTEND, "profile.html")

@app.route("/reports")
def reports():
    return send_from_directory(FRONTEND, "reports.html")

@app.route("/css/<path:filename>")
def css(filename):
    return send_from_directory(os.path.join(FRONTEND, "css"), filename)

@app.route("/js/<path:filename>")
def js(filename):
    return send_from_directory(os.path.join(FRONTEND, "js"), filename)

@app.route("/predict", methods=["POST"])
def predict():

    data = request.get_json()

    crop = data["crop"]
    temp = float(data["temp"])
    humidity = float(data["humidity"])
    rainfall = float(data["rainfall"])
    ph = float(data["ph"])

    prediction = round(
        (temp * 0.08) +
        (humidity * 0.02) +
        (rainfall * 0.01) +
        (ph * 0.5), 2
    )

    record = {
        "crop": crop,
        "temp": temp,
        "humidity": humidity,
        "rainfall": rainfall,
        "ph": ph,
        "yield": prediction
    }

    history.append(record)

    return jsonify({
        "crop": crop,
        "yield": prediction,
        "message": "Prediction Successful!"
    })

@app.route("/getHistory")
def get_history():
    return jsonify(history)

if __name__ == "__main__":
    app.run(debug=True)