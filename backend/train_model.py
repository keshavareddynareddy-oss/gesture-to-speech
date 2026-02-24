import os
import numpy as np
from PIL import Image
from sklearn.svm import SVC
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
from sklearn.preprocessing import StandardScaler
import joblib

# Absolute base directory (backend/)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

DATASET_PATH = os.path.join(BASE_DIR, "dataset", "asl_alphabet_train")
MODEL_PATH = os.path.join(BASE_DIR, "gesture_model.pkl")
SCALER_PATH = os.path.join(BASE_DIR, "scaler.pkl")


def load_data():
    X = []
    y = []

    print("Loading images...")

    for label in os.listdir(DATASET_PATH):
        folder = os.path.join(DATASET_PATH, label)

        if not os.path.isdir(folder):
            continue

        images = os.listdir(folder)

        for img_name in images[:100]:  # increase for better accuracy
            img_path = os.path.join(folder, img_name)

            try:
                img = Image.open(img_path).resize((64, 64)).convert("L")
                img_array = np.array(img) / 255.0  # normalize
                X.append(img_array.flatten())
                y.append(label)
            except:
                continue

    return np.array(X), np.array(y)


def train_model():
    X, y = load_data()

    print("Splitting dataset...")
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )

    print("Scaling features...")
    scaler = StandardScaler()
    X_train = scaler.fit_transform(X_train)
    X_test = scaler.transform(X_test)

    print("Training model...")
    model = SVC(kernel="linear", probability=True)
    model.fit(X_train, y_train)

    print("Evaluating model...")
    y_pred = model.predict(X_test)
    print(classification_report(y_test, y_pred))

    joblib.dump(model, MODEL_PATH)
    joblib.dump(scaler, SCALER_PATH)

    print("Model saved at:", MODEL_PATH)
    print("Scaler saved at:", SCALER_PATH)


if __name__ == "__main__":
    train_model()