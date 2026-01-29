from flask import Flask, request, jsonify
from flask_cors import CORS
import base64
import pyttsx3
from database import SessionLocal, Gesture, History
from model import predict_gesture

app = Flask(__name__)

# ✅ Proper CORS setup
CORS(app, resources={r"/*": {"origins": "*"}})

engine = pyttsx3.init()

@app.route("/predict", methods=["POST"])
def predict():
    data = request.json.get("image")
    if not data:
        return jsonify({"error": "No image provided"}), 400

    image_bytes = base64.b64decode(data.split(",")[1])

    gesture_name = predict_gesture(image_bytes)

    db = SessionLocal()
    gesture = db.query(Gesture).filter_by(name=gesture_name).first()

    if gesture:
        text = gesture.output_text
    else:
        text = "Unknown gesture"

    # Save history
    history = History(gesture=gesture_name, text=text)
    db.add(history)
    db.commit()
    db.close()

    # Text to Speech
    engine.say(text)
    engine.runAndWait()

    return jsonify({"text": text})

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)
