import os
import requests
import pandas as pd
from tqdm import tqdm

OUT_DIR = "data/fitzpatrick"
CSV_URL = "https://raw.githubusercontent.com/mattgroh/fitzpatrick17k/main/fitzpatrick17k.csv"

os.makedirs(OUT_DIR, exist_ok=True)

print("Downloading Fitzpatrick CSV...")
r = requests.get(CSV_URL)
r.raise_for_status()
csv_path = os.path.join(OUT_DIR, "fitzpatrick17k.csv")
open(csv_path, "wb").write(r.content)
print("CSV downloaded.")

df = pd.read_csv(csv_path)
print("Total rows:", len(df))

limit = input("How many images to download? (Recommended 2000 first time): ").strip()
if limit.lower() == "all":
    limit = len(df)
else:
    limit = int(limit)

downloaded = 0
for i, row in tqdm(df.iterrows(), total=limit):
    if downloaded >= limit:
        break
    url = row.get("url")
    if not isinstance(url, str):
        continue
    try:
        img_path = os.path.join(OUT_DIR, f"{i}.jpg")
        if os.path.exists(img_path):
            downloaded += 1
            continue
        resp = requests.get(url, timeout=5)
        if resp.status_code == 200 and len(resp.content) > 2000:
            with open(img_path, "wb") as f:
                f.write(resp.content)
            downloaded += 1
    except:
        continue

print(f"Downloaded {downloaded} images.")
