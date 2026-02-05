import os
import numpy as np
from PIL import Image
from sklearn.svm import SVC
import joblib

# Absolute base directory (backend/)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Correct dataset path
DATASET_PATH = os.path.join(BASE_DIR, "dataset", "asl_alphabet_train")

# Where model will be saved
MODEL_PATH = os.path.join(BASE_DIR, "gesture_model.pkl")


def load_data():
    X = []
    y = []

    print("Loading images...")

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
    X, y = load_data()

    print("Training model...")
    model = SVC(kernel="linear", probability=True)
    model.fit(X, y)

    joblib.dump(model, MODEL_PATH)
    print("Model saved at:", MODEL_PATH)


if __name__ == "__main__":
    train_model()
