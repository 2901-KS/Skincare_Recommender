import os
import subprocess

OUT_DIR = "data/acne"
KAGGLE_SLUGS = ["jincyjis/acne04", "manuelhettich/acne04"]

os.makedirs(OUT_DIR, exist_ok=True)

success = False

for slug in KAGGLE_SLUGS:
    print("Trying:", slug)
    cmd = ["kaggle", "datasets", "download", "-d", slug, "-p", OUT_DIR, "--unzip"]
    res = subprocess.run(cmd)
    if res.returncode == 0:
        print("ACNE04 downloaded successfully.")
        success = True
        break

if not success:
    print("ACNE04 not available from Kaggle. Download manually from:")
    print("https://huggingface.co/datasets/ManuelHettich/acne04")
