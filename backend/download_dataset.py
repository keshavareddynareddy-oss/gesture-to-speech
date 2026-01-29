import kagglehub

# Download latest version of the dataset
path = kagglehub.dataset_download("grassknoted/asl-alphabet")

print("Path to dataset files:", path)
