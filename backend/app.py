from flask import Flask, request, jsonify
from flask_cors import CORS
import base64
import pyttsx3
import threading
import time
from database import SessionLocal, Gesture, History
from model import predict_gesture

app = Flask(__name__)

# CORS
CORS(app, resources={r"/*": {"origins": "*"}})

# Text-to-Speech Engine
engine = pyttsx3.init()

# Prevent overlapping speech
speech_lock = threading.Lock()
last_spoken = ""

# Gesture smoothing variables
last_known_gesture = None
last_seen_time = time.time()
WAIT_SECONDS = 3   # wait before declaring unknown

def speak(text):
    global last_spoken

    if text == last_spoken:
        return

    def run_speech():
        with speech_lock:
            try:
                engine.stop()
                engine.say(text)
                engine.runAndWait()
            except RuntimeError:
                pass

    threading.Thread(target=run_speech).start()
    last_spoken = text


@app.route("/predict", methods=["POST"])
def predict():
    global last_known_gesture, last_seen_time

    data = request.json.get("image")
    if not data:
        return jsonify({"error": "No image provided"}), 400

    image_bytes = base64.b64decode(data.split(",")[1])

    # MODEL PREDICTION
    gesture_name = str(predict_gesture(image_bytes)).strip()


    # SMOOTHING LOGIC
    current_time = time.time()

    if gesture_name != "Unknown":
        last_known_gesture = gesture_name
        last_seen_time = current_time
    else:
        # If still within wait time, reuse last known gesture
        if last_known_gesture and (current_time - last_seen_time < WAIT_SECONDS):
            gesture_name = last_known_gesture

    # DATABASE LOOKUP
    db = SessionLocal()
    gesture = db.query(Gesture).filter_by(name=gesture_name).first()

    if gesture:
        text = gesture.output_text
    else:
        text = "Unknown gesture"

    # SAVE HISTORY
    history = History(gesture=gesture_name, text=text)
    db.add(history)
    db.commit()
    db.close()

    # TEXT TO SPEECH
    speak(text)

    return jsonify({"text": text})


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)
