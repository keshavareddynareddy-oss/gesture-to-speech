import io
import os
import numpy as np
from PIL import Image
import joblib

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

MODEL_PATH = os.path.join(BASE_DIR, "gesture_model.pkl")
SCALER_PATH = os.path.join(BASE_DIR, "scaler.pkl")

if not os.path.exists(MODEL_PATH):
    raise FileNotFoundError(f"Model not found: {MODEL_PATH}")

if not os.path.exists(SCALER_PATH):
    raise FileNotFoundError(f"Scaler not found: {SCALER_PATH}")

model = joblib.load(MODEL_PATH)
scaler = joblib.load(SCALER_PATH)

print("Gesture model loaded with scaler")


def predict_gesture(image_bytes):
    """
    Convert image bytes to prediction with confidence filtering
    """

    img = Image.open(io.BytesIO(image_bytes)) \
               .resize((64, 64)) \
               .convert("L")

    arr = np.array(img) / 255.0  # normalize
    arr = arr.flatten().reshape(1, -1)

    # Apply scaling
    arr_scaled = scaler.transform(arr)

    try:
        probabilities = model.predict_proba(arr_scaled)[0]
        confidence = np.max(probabilities)
        prediction = model.predict(arr_scaled)[0]

        if confidence < 0.75:
            return "Unknown"

        return prediction

    except Exception:
        prediction = model.predict(arr_scaled)[0]
        return prediction