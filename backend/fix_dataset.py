import os
import shutil

# Create dataset folder if not exists
os.makedirs(r"C:\gesture-to-speech\backend\dataset", exist_ok=True)

src = r"C:\Users\MRCE DIGITAL.LIB\.cache\kagglehub\datasets\grassknoted\asl-alphabet\versions\1\asl_alphabet_train\asl_alphabet_train"
dst = r"C:\gesture-to-speech\backend\dataset\asl_alphabet_train"

# ---- CHECK IF SOURCE EXISTS ----
if not os.path.exists(src):
    print("Source dataset not found! Check the path.")
    exit()

# ---- COPY ONLY IF NOT ALREADY COPIED ----
if not os.path.exists(dst):
    shutil.copytree(src, dst)
    print("Dataset copied successfully!")
else:
    print("Dataset already exists, skipping copy.")

# ---- VERIFY CLASSES (ONLY FOLDERS) ----
DATASET_PATH = dst
classes = [
    f for f in os.listdir(DATASET_PATH)
    if os.path.isdir(os.path.join(DATASET_PATH, f))
]

print("Classes:", classes)
print("Total classes:", len(classes))
print("Dataset structure fixed!")
