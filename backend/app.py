from flask import Flask, request, jsonify
from flask_cors import CORS
import base64
import time
import pyttsx3

from database import SessionLocal, Gesture, History
from model import predict_gesture

app = Flask(__name__)
CORS(app)

# ==========================
# Stability + Sentence State
# ==========================
last_prediction = None
stable_count = 0
last_confirmed_gesture = None
last_confirmed_time = 0

# 🔥 Tuned for real webcam stability
STABLE_THRESHOLD = 2
COOLDOWN_SECONDS = 1.0

# Sentence memory
current_sentence = ""

# Text to Speech Engine
engine = pyttsx3.init()


@app.route("/predict", methods=["POST"])
def predict():
    global last_prediction, stable_count
    global last_confirmed_gesture, last_confirmed_time
    global current_sentence

    data = request.json.get("image")
    if not data:
        return jsonify({"error": "No image provided"}), 400

    try:
        image_bytes = base64.b64decode(data.split(",")[1])
    except Exception:
        return jsonify({"error": "Invalid image data"}), 400

    gesture_name = str(predict_gesture(image_bytes)).strip()

    # ==========================
    # Unknown Reset
    # ==========================
    if gesture_name == "Unknown":
        stable_count = max(0, stable_count - 1)
        print("Gesture: Unknown | Stable:", stable_count)
        return jsonify({
            "gesture": "Unknown",
            "confirmed": False,
            "sentence": current_sentence
        })

    # ==========================
    # Smooth Stability Logic
    # ==========================
    if gesture_name == last_prediction:
        stable_count += 1
    else:
        # Instead of full reset, decrease slowly
        stable_count = max(1, stable_count - 1)

    last_prediction = gesture_name

    confirmed = False

    # ==========================
    # Confirmation Logic
    # ==========================
    if stable_count >= STABLE_THRESHOLD:
        current_time = time.time()

        if not (
            gesture_name == last_confirmed_gesture and
            current_time - last_confirmed_time < COOLDOWN_SECONDS
        ):
            confirmed = True
            last_confirmed_gesture = gesture_name
            last_confirmed_time = current_time

            if gesture_name == "Space":
                current_sentence += " "
            elif gesture_name == "Delete":
                current_sentence = current_sentence[:-1]
            elif gesture_name == "Clear":
                current_sentence = ""
            elif gesture_name == "Speak":
                engine.say(current_sentence)
                engine.runAndWait()
            else:
                current_sentence += gesture_name

            # Save to history
            db = SessionLocal()
            try:
                history = History(gesture=gesture_name, text=current_sentence)
                db.add(history)
                db.commit()
            except Exception as e:
                db.rollback()
                print("DB Error:", e)
            finally:
                db.close()

    # 🔥 Debug print (VERY IMPORTANT)
    print(
        "Gesture:", gesture_name,
        "| Stable:", stable_count,
        "| Confirmed:", confirmed,
        "| Sentence:", current_sentence
    )

    return jsonify({
        "gesture": gesture_name,
        "confirmed": confirmed,
        "sentence": current_sentence
    })


@app.route("/reset", methods=["POST"])
def reset():
    global current_sentence
    current_sentence = ""
    print("Sentence Reset")
    return jsonify({"message": "Sentence cleared"})


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)