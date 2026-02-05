import io
import os
import numpy as np
from PIL import Image
import joblib

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(BASE_DIR, "gesture_model.pkl")

# Load model once
if not os.path.exists(MODEL_PATH):
    raise FileNotFoundError(f"Model not found: {MODEL_PATH}")

model = joblib.load(MODEL_PATH)
print("Gesture model loaded")

def predict_gesture(image_bytes):
    """
    Convert image bytes to prediction
    """

    img = Image.open(io.BytesIO(image_bytes)) \
               .resize((64, 64)) \
               .convert("L")

    arr = np.array(img).flatten().reshape(1, -1)

    prediction = model.predict(arr)[0]
    return prediction
