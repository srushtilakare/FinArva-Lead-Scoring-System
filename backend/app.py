import os
import pickle
import subprocess
from flask import Flask, request, jsonify

app = Flask(__name__)

MODEL_PATH = "backend/model/lead_model.pkl"
ENCODER_PATH = "backend/model/location_encoder.pkl"

# If model files missing, train the model
if not os.path.exists(MODEL_PATH) or not os.path.exists(ENCODER_PATH):
    subprocess.run(["python", "train_model.py"])

# Load model and encoder
with open(MODEL_PATH, "rb") as f:
    model = pickle.load(f)

with open(ENCODER_PATH, "rb") as f:
    location_encoder = pickle.load(f)

@app.route("/", methods=["GET"])
def home():
    return jsonify({"message": "Lead Scoring System API is running."})

@app.route("/predict", methods=["POST"])
def predict():
    try:
        data = request.get_json()

        # Extract features
        age = data.get("age")
        location = data.get("location")
        income = data.get("income")
        interaction_count = data.get("interaction_count")
        interest_score = data.get("interest_score")

        # Basic input validation
        if None in [age, location, income, interaction_count, interest_score]:
            return jsonify({"error": "Missing input fields"}), 400

        # Encode location
        try:
            location_encoded = location_encoder.transform([location])[0]
        except ValueError:
            return jsonify({"error": f"Unknown location value: {location}"}), 400

        # Prepare feature vector in the order used during training
        features = [[
            age,
            location_encoded,
            income,
            interaction_count,
            interest_score
        ]]

        # Predict class (0 or 1)
        prediction = model.predict(features)[0]
        # Predict probability of class 1 (converted)
        proba = model.predict_proba(features)[0][1]

        return jsonify({
            "converted_prediction": int(prediction),
            "conversion_probability": round(proba, 4)
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
