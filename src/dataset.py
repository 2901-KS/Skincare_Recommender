import os
from PIL import Image
from torch.utils.data import Dataset
import torchvision.transforms as T
import pandas as pd

def get_transforms(train=True):
    if train:
        return T.Compose([
            T.Resize((256,256)),
            T.RandomResizedCrop(224, scale=(0.8,1.0)),
            T.RandomHorizontalFlip(),
            T.ColorJitter(0.1,0.1,0.05,0.02),
            T.ToTensor(),
            T.Normalize([0.485,0.456,0.406],[0.229,0.224,0.225])
        ])
    else:
        return T.Compose([
            T.Resize((224,224)),
            T.ToTensor(),
            T.Normalize([0.485,0.456,0.406],[0.229,0.224,0.225])
        ])

class ImageFolderDataset(Dataset):
    def __init__(self, root=None, csv_path=None, split="train", transform=None):
        self.transform = transform or get_transforms(train=(split=="train"))
        self.items = []

        if csv_path:
            df = pd.read_csv(csv_path)
            for _, r in df.iterrows():
                img = r["image_path"]
                label = int(r["label"])
                self.items.append((img, label))

        else:
            split_dir = os.path.join(root, split)
            classes = sorted([d for d in os.listdir(split_dir) if os.path.isdir(os.path.join(split_dir,d))])
            class_to_idx = {c:i for i,c in enumerate(classes)}

            for c in classes:
                folder = os.path.join(split_dir, c)
                for f in os.listdir(folder):
                    if f.lower().endswith(("jpg","jpeg","png")):
                        self.items.append((os.path.join(folder,f), class_to_idx[c]))

    def __len__(self): return len(self.items)

    def __getitem__(self, idx):
        path, label = self.items[idx]
        img = Image.open(path).convert("RGB")
        return self.transform(img), label
