import os
import numpy as np
from PIL import Image
from sklearn.svm import SVC
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import classification_report
import joblib

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

        for img_name in os.listdir(folder)[:100]:
            img_path = os.path.join(folder, img_name)

            try:
                img = Image.open(img_path).resize((64, 64)).convert("L")
                img_array = np.array(img) / 255.0
                X.append(img_array.flatten())
                y.append(label)
            except:
                continue

    return np.array(X), np.array(y)


def train_model():
    X, y = load_data()

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )

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

    print("Model and scaler saved successfully!")


if __name__ == "__main__":
    train_model()