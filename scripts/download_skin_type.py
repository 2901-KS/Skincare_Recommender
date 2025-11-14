import os
import subprocess

OUT_DIR = "data/skin_type"
DATASET = "shakyadissanayake/oily-dry-and-normal-skin-types-dataset"

os.makedirs(OUT_DIR, exist_ok=True)

print("Downloading Skin Type dataset from Kaggle...")
cmd = ["kaggle", "datasets", "download", "-d", DATASET, "-p", OUT_DIR, "--unzip"]
res = subprocess.run(cmd)

if res.returncode == 0:
    print("Skin type dataset downloaded successfully.")
else:
    print("Error downloading dataset. Ensure Kaggle API is configured correctly.")
