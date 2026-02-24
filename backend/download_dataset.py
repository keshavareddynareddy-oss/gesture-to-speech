import os
import shutil
import kagglehub

# Download dataset
path = kagglehub.dataset_download("grassknoted/asl-alphabet")
print("Downloaded to:", path)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATASET_DIR = os.path.join(BASE_DIR, "dataset")
dst = os.path.join(DATASET_DIR, "asl_alphabet_train")

# Try to locate dataset automatically
possible_src = [
    os.path.join(path, "asl_alphabet_train", "asl_alphabet_train"),
    os.path.join(path, "asl_alphabet_train"),
]

src = None
for p in possible_src:
    if os.path.exists(p):
        src = p
        break

if not src:
    print("Could not locate dataset structure automatically.")
    exit()

os.makedirs(DATASET_DIR, exist_ok=True)

if not os.path.exists(dst):
    shutil.copytree(src, dst)
    print("Dataset copied successfully!")
else:
    print("Dataset already exists.")

print("Setup complete.")