import os
import requests
import pandas as pd
from tqdm import tqdm

OUT_DIR = "data/fitzpatrick"
CSV_URL = "https://raw.githubusercontent.com/mattgroh/fitzpatrick17k/main/fitzpatrick17k.csv"

os.makedirs(OUT_DIR, exist_ok=True)

print("📥 Downloading Fitzpatrick CSV...")
csv_data = requests.get(CSV_URL)
csv_data.raise_for_status()

csv_path = os.path.join(OUT_DIR, "fitzpatrick17k.csv")
with open(csv_path, "wb") as f:
    f.write(csv_data.content)

print("✔ CSV downloaded successfully.")

df = pd.read_csv(csv_path)
print("Total rows in CSV:", len(df))

LIMIT = 2000  # Fixed for demo

print(f"📸 Starting download of {LIMIT} images...\n")

downloaded = 0
skipped = 0

for idx, row in tqdm(df.iterrows(), total=LIMIT):
    if downloaded >= LIMIT:
        break

    url = row["url"]

    if not isinstance(url, str) or len(url) < 5:
        skipped += 1
        continue

    filename = os.path.join(OUT_DIR, f"{idx}.jpg")

    # If already exists, skip
    if os.path.exists(filename):
        downloaded += 1
        continue

    try:
        img = requests.get(url, timeout=8)
        if img.status_code == 200 and len(img.content) > 5000:  # Avoid broken tiny files
            with open(filename, "wb") as f:
                f.write(img.content)
            downloaded += 1
        else:
            skipped += 1
    except:
        skipped += 1

print(f"\n✅ DONE!")
print(f"Downloaded: {downloaded}")
print(f"Skipped: {skipped}")
