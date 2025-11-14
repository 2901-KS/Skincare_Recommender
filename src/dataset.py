import os
import shutil
import random
from PIL import Image
from torch.utils.data import Dataset
import torchvision.transforms as T

# -----------------------------
# IMAGE TRANSFORMS
# -----------------------------
def get_transforms(train):
    if train:
        return T.Compose([
            T.Resize((224, 224)),
            T.RandomHorizontalFlip(),
            T.RandomRotation(10),
            T.ToTensor(),
        ])
    else:
        return T.Compose([
            T.Resize((224, 224)),
            T.ToTensor(),
        ])

# -----------------------------
# GENERIC IMAGEFOLDER DATASET
# -----------------------------
class ImageFolderDataset(Dataset):
    def __init__(self, root, split, transform=None):
        self.transform = transform
        self.root = os.path.join(root, split)

        self.classes = sorted([
            d for d in os.listdir(self.root)
            if os.path.isdir(os.path.join(self.root, d))
        ])

        self.img_paths = []
        self.labels = []

        for idx, cls in enumerate(self.classes):
            folder = os.path.join(self.root, cls)
            for f in os.listdir(folder):
                if f.lower().endswith((".jpg", ".jpeg", ".png")):
                    self.img_paths.append(os.path.join(folder, f))
                    self.labels.append(idx)

        print(f"Loaded {len(self.img_paths)} images for {split}")

    def __len__(self):
        return len(self.img_paths)

    def __getitem__(self, idx):
        img = Image.open(self.img_paths[idx]).convert("RGB")
        if self.transform:
            img = self.transform(img)
        return img, self.labels[idx]

# -----------------------------
# ACNE DATASET PREPARATION
# -----------------------------
def prepare_acne_dataset():
    ROOT = "data/acne"
    IMG_DIR = os.path.join(ROOT, "JPEGImages")
    TRAIN_DIR = os.path.join(ROOT, "train")
    VAL_DIR = os.path.join(ROOT, "val")

    print("Preparing ACNE dataset...")

    if os.path.exists(TRAIN_DIR):
        shutil.rmtree(TRAIN_DIR)
    if os.path.exists(VAL_DIR):
        shutil.rmtree(VAL_DIR)

    for cls in ["level0", "level1", "level2", "level3"]:
        os.makedirs(os.path.join(TRAIN_DIR, cls), exist_ok=True)
        os.makedirs(os.path.join(VAL_DIR, cls), exist_ok=True)

    images = [
        f for f in os.listdir(IMG_DIR)
        if f.lower().endswith((".jpg", ".jpeg", ".png"))
    ]

    if len(images) == 0:
        print("❌ ERROR: No images found in JPEGImages!")
        return

    counts = {"level0": 0, "level1": 0, "level2": 0, "level3": 0}

    for img in images:
        name = img.lower()

        if "level0" in name:
            cls = "level0"
        elif "level1" in name:
            cls = "level1"
        elif "level2" in name:
            cls = "level2"
        elif "level3" in name:
            cls = "level3"
        else:
            print("Skipping unrecognized:", img)
            continue

        dest_root = TRAIN_DIR if random.random() < 0.85 else VAL_DIR
        shutil.copy(os.path.join(IMG_DIR, img), os.path.join(dest_root, cls))
        counts[cls] += 1

    print("✨ Dataset prepared successfully!")
    print("Counts:", counts)


if __name__ == "__main__":
    prepare_acne_dataset()
