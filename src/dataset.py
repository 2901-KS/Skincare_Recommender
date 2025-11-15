import os
import shutil
import random
from PIL import Image
from torch.utils.data import Dataset
import torchvision.transforms as T

# --------------------------------------------------
# 1️⃣ IMAGE TRANSFORMS (BETTER for ALL datasets)
# --------------------------------------------------
def get_transforms(train=True):
    """
    - Strong augmentation for train
    - Soft preprocessing for val/test
    - Skin-friendly normalization
    """
    if train:
        return T.Compose([
            T.Resize((256, 256)),
            T.RandomResizedCrop(224, scale=(0.7, 1.0)),
            T.RandomHorizontalFlip(),
            T.RandomRotation(15),
            T.ColorJitter(brightness=0.3, contrast=0.3, saturation=0.2),
            T.ToTensor(),
            T.Normalize(mean=[0.55, 0.45, 0.40], std=[0.25, 0.25, 0.25])
        ])
    else:
        return T.Compose([
            T.Resize((256, 256)),
            T.CenterCrop(224),
            T.ToTensor(),
            T.Normalize(mean=[0.55, 0.45, 0.40], std=[0.25, 0.25, 0.25])
        ])

# --------------------------------------------------
# 2️⃣ GENERIC IMAGE FOLDER DATASET 
# (Works for Acne, Skin Type, Skin Tone)
# --------------------------------------------------
class ImageFolderDataset(Dataset):
    def __init__(self, root_dir, split="train", transform=None):
        """
        root_dir: e.g. data/acne or data/skin_type
        split: 'train', 'val', 'valid', 'test'
        """
        self.root = os.path.join(root_dir, split)
        self.transform = transform
        self.samples = []

        # all classes inside split folder
        classes = sorted([
            d for d in os.listdir(self.root)
            if os.path.isdir(os.path.join(self.root, d))
        ])
        self.class_to_idx = {cls: idx for idx, cls in enumerate(classes)}

        for cls in classes:
            cls_folder = os.path.join(self.root, cls)
            for f in os.listdir(cls_folder):
                if f.lower().endswith((".jpg", ".jpeg", ".png")):
                    self.samples.append((os.path.join(cls_folder, f), self.class_to_idx[cls]))

        print(f"Loaded {len(self.samples)} images for {split}")

    def __len__(self):
        return len(self.samples)

    def __getitem__(self, idx):
        path, label = self.samples[idx]
        img = Image.open(path).convert("RGB")
        if self.transform:
            img = self.transform(img)
        return img, label

# --------------------------------------------------
# 3️⃣ ACNE DATASET PREPARATION
# --------------------------------------------------
def prepare_acne_dataset():
    ROOT = "data/acne"
    IMG_DIR = os.path.join(ROOT, "JPEGImages")
    TRAIN_DIR = os.path.join(ROOT, "train")
    VAL_DIR = os.path.join(ROOT, "val")

    print("Preparing ACNE dataset...")

    # clear old structure
    if os.path.exists(TRAIN_DIR):
        shutil.rmtree(TRAIN_DIR)
    if os.path.exists(VAL_DIR):
        shutil.rmtree(VAL_DIR)

    # create class folders
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

        dest = TRAIN_DIR if random.random() < 0.85 else VAL_DIR
        shutil.copy(os.path.join(IMG_DIR, img), os.path.join(dest, cls))
        counts[cls] += 1

    print("✨ ACNE dataset prepared successfully!")
    print("Counts:", counts)


if __name__ == "__main__":
    prepare_acne_dataset()
