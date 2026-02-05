import os
import cv2
import numpy as np
from sklearn.svm import SVC
from sklearn.model_selection import train_test_split
import joblib

DATASET_PATH = "asl_alphabet_train"
IMG_SIZE = 64

X = []
y = []

print("Loading images...")

for label in os.listdir(DATASET_PATH):
    folder_path = os.path.join(DATASET_PATH, label)

    for img_name in os.listdir(folder_path):
        img_path = os.path.join(folder_path, img_name)

        img = cv2.imread(img_path)
        if img is None:
            continue

        img = cv2.resize(img, (IMG_SIZE, IMG_SIZE))
        img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        img = img.flatten()

        X.append(img)
        y.append(label)

X = np.array(X)
y = np.array(y)

print("Splitting dataset...")
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2
)

print("Training model...")
model = SVC(kernel="linear", probability=True)
model.fit(X_train, y_train)

accuracy = model.score(X_test, y_test)
print("Accuracy:", accuracy)

joblib.dump(model, "model.pkl")
print("Model saved as model.pkl")
