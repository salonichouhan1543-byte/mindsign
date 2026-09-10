from flask import Flask, request, jsonify
from flask_cors import CORS
import csv
import os

app = Flask(__name__)
CORS(app)  # allows our website (different port) to talk to this server

DATA_DIR = os.path.join(os.path.dirname(__file__), "data")
DATA_FILE = os.path.join(DATA_DIR, "signs.csv")

# Make sure the data folder and file exist
os.makedirs(DATA_DIR, exist_ok=True)
if not os.path.exists(DATA_FILE):
    with open(DATA_FILE, "w", newline="") as f:
        writer = csv.writer(f)
        # 21 landmarks x (x, y, z) = 63 columns, plus the label
        header = []
        for i in range(21):
            header += [f"x{i}", f"y{i}", f"z{i}"]
        header.append("label")
        writer.writerow(header)


@app.route("/")
def home():
    return "Sign language backend is running."


@app.route("/save", methods=["POST"])
def save_sample():
    data = request.get_json()

    landmarks = data.get("landmarks")  # expect a flat list of 63 numbers
    label = data.get("label")          # expect a string, e.g. "hello"

    if not landmarks or not label:
        return jsonify({"error": "landmarks and label are required"}), 400

    if len(landmarks) != 63:
        return jsonify({"error": f"expected 63 values, got {len(landmarks)}"}), 400

    with open(DATA_FILE, "a", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(landmarks + [label])

    return jsonify({"status": "saved", "label": label})


@app.route("/predict", methods=["POST"])
def predict_sign():
    # Placeholder for now — we'll wire this up after training a model
    return jsonify({"prediction": "model not trained yet"})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)