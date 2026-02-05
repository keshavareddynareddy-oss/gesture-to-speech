import io
import os
import numpy as np
from PIL import Image
from sklearn.svm import SVC
import joblib

MODEL_PATH = "gesture_model.pkl"
DATASET_PATH = "dataset/asl_alphabet_train"

def load_data():
    X = []
    y = []

    for label in os.listdir(DATASET_PATH):
        folder = os.path.join(DATASET_PATH, label)
        if not os.path.isdir(folder):
            continue

        for img_name in os.listdir(folder)[:50]:  # limit for speed
            img_path = os.path.join(folder, img_name)
            img = Image.open(img_path).resize((64, 64)).convert("L")
            X.append(np.array(img).flatten())
            y.append(label)

    return np.array(X), np.array(y)

def train_model():
    print("Loading dataset...")
    X, y = load_data()

    print("Training model...")
    model = SVC()
    model.fit(X, y)

    joblib.dump(model, MODEL_PATH)
    print("Model saved!")

def predict_gesture(image_bytes):
    model = joblib.load(MODEL_PATH)

    img = Image.open(io.BytesIO(image_bytes)).resize((64, 64)).convert("L")
    arr = np.array(img).flatten().reshape(1, -1)

    prediction = model.predict(arr)[0]
    return prediction


if __name__ == "__main__":
    train_model()
