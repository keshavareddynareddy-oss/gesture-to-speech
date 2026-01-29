import os
import shutil

# Create dataset folder if not exists
os.makedirs(r"C:\gesture-to-speech\backend\dataset", exist_ok=True)

src = r"C:\Users\MRCE DIGITAL.LIB\.cache\kagglehub\datasets\grassknoted\asl-alphabet\versions\1\asl_alphabet_train\asl_alphabet_train"
dst = r"C:\gesture-to-speech\backend\dataset\asl_alphabet_train"

# Copy dataset and overwrite if exists
shutil.copytree(src, dst, dirs_exist_ok=True)

print("Dataset structure fixed!")

# Verify classes
DATASET_PATH = dst
print(os.listdir(DATASET_PATH))
print("Total classes:", len(os.listdir(DATASET_PATH)))
