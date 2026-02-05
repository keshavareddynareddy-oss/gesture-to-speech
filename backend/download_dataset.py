import os
import shutil
import kagglehub

# Download dataset
path = kagglehub.dataset_download("grassknoted/asl-alphabet")
print("Downloaded to:", path)

src = os.path.join(path, "asl_alphabet_train", "asl_alphabet_train")
dst = r"C:\gesture-to-speech\backend\dataset\asl_alphabet_train"

os.makedirs(r"C:\gesture-to-speech\backend\dataset", exist_ok=True)

if not os.path.exists(dst):
    shutil.copytree(src, dst)
    print("Dataset copied!")
else:
    print("Dataset already exists.")

print("Setup complete.")
