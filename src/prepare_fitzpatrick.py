import os
import shutil
import pandas as pd
from sklearn.model_selection import train_test_split

DATA_DIR = "data/fitzpatrick"
CSV_PATH = os.path.join(DATA_DIR, "fitzpatrick17k.csv")

# 6 skin tone classes (0–5)
CLASS_NAMES = ["type1", "type2", "type3", "type4", "type5", "type6"]

def prepare_fitzpatrick_dataset():
    print("Loading CSV...")
    df = pd.read_csv(CSV_PATH)

    # Filter only downloaded images
    df = df[df.index < 2000]  # Only first 2000 rows

    print("Mapping labels...")
    df["label"] = df["fitzpatrick_scale"] - 1   # Convert 1–6 → 0–5

    # Create folders
    for split in ["train", "val"]:
        for c in CLASS_NAMES:
            os.makedirs(os.path.join(DATA_DIR, split, c), exist_ok=True)

    print("Splitting dataset...")
    train_df, val_df = train_test_split(df, test_size=0.2, stratify=df["label"], random_state=42)

    # Copy images
    def copy_files(df, split):
        for idx, row in df.iterrows():
            img_name = f"{idx}.jpg"
            src = os.path.join(DATA_DIR, img_name)
            cls = CLASS_NAMES[row["label"]]
            dst = os.path.join(DATA_DIR, split, cls, img_name)

            if os.path.exists(src):
                shutil.copy(src, dst)

    print("Copying train files...")
    copy_files(train_df, "train")

    print("Copying val files...")
    copy_files(val_df, "val")

    print("\n✅ Fitzpatrick dataset prepared successfully!")

if __name__ == "__main__":
    prepare_fitzpatrick_dataset()
