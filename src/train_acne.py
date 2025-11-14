import os
import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader
from sklearn.metrics import accuracy_score

from dataset import ImageFolderDataset, get_transforms, prepare_acne_dataset
from model_acne import build_acne_model

device = "cuda" if torch.cuda.is_available() else "cpu"

# STEP 1: Prepare dataset
prepare_acne_dataset()

# STEP 2: Load dataset
train_ds = ImageFolderDataset("data/acne", split="train", transform=get_transforms(True))
val_ds   = ImageFolderDataset("data/acne", split="val", transform=get_transforms(False))

train_loader = DataLoader(train_ds, batch_size=16, shuffle=True)
val_loader   = DataLoader(val_ds, batch_size=16, shuffle=False)

# STEP 3: Model
model = build_acne_model(num_classes=4).to(device)
opt = optim.Adam(model.parameters(), lr=1e-4)
crit = nn.CrossEntropyLoss()

best = 0

for epoch in range(10):
    print(f"\nEpoch {epoch+1}")

    model.train()
    for imgs, labels in train_loader:
        imgs, labels = imgs.to(device), labels.to(device)
        opt.zero_grad()
        out = model(imgs)
        loss = crit(out, labels)
        loss.backward()
        opt.step()

    model.eval()
    preds, trues = [], []
    with torch.no_grad():
        for imgs, labels in val_loader:
            imgs = imgs.to(device)
            out = model(imgs)
            preds.extend(out.argmax(1).cpu().tolist())
            trues.extend(labels.tolist())

    acc = accuracy_score(trues, preds)
    print(f"Val Acc = {acc:.4f}")

    if acc > best:
        best = acc
        os.makedirs("models", exist_ok=True)
        torch.save(model.state_dict(), "models/acne.pth")
        print("Saved best model!")
