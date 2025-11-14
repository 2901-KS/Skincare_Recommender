import os
import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader
from sklearn.metrics import accuracy_score
from torchvision import models
from dataset import ImageFolderDataset, get_transforms

device = "cuda" if torch.cuda.is_available() else "cpu"
print("Using:", device)

DATA_DIR = "data/fitzpatrick"
NUM_CLASSES = 6  # type1 to type6

# -----------------------------
# LOAD DATASETS
# -----------------------------
print("Loading datasets...")
train_ds = ImageFolderDataset(DATA_DIR, split="train", transform=get_transforms(True))
val_ds   = ImageFolderDataset(DATA_DIR, split="val",   transform=get_transforms(False))

print(f"Train samples: {len(train_ds)}")
print(f"Val samples  : {len(val_ds)}")

train_loader = DataLoader(train_ds, batch_size=32, shuffle=True)
val_loader   = DataLoader(val_ds, batch_size=32, shuffle=False)

# -----------------------------
# MODEL
# -----------------------------
print("Loading ResNet18...")
from model_skin_tone import build_skin_tone_model
model = build_skin_tone_model(num_classes=6, pretrained=True).to(device)


opt = optim.Adam(model.parameters(), lr=1e-4)
crit = nn.CrossEntropyLoss()

best_acc = 0
epochs = 10

# -----------------------------
# TRAINING LOOP
# -----------------------------
for epoch in range(epochs):
    print(f"\nEpoch {epoch+1}/{epochs}")

    model.train()
    for imgs, labels in train_loader:
        imgs, labels = imgs.to(device), labels.to(device)

        opt.zero_grad()
        preds = model(imgs)
        loss = crit(preds, labels)
        loss.backward()
        opt.step()

    # -----------------------------
    # VALIDATION
    # -----------------------------
    model.eval()
    y_true, y_pred = [], []

    with torch.no_grad():
        for imgs, labels in val_loader:
            imgs = imgs.to(device)
            outputs = model(imgs)
            y_pred.extend(outputs.argmax(1).cpu().tolist())
            y_true.extend(labels.tolist())

    acc = accuracy_score(y_true, y_pred)
    print(f"Validation Accuracy: {acc:.4f}")

    if acc > best_acc:
        best_acc = acc
        os.makedirs("models", exist_ok=True)
        torch.save(model.state_dict(), "models/skin_tone.pth")
        print("🔥 Saved new BEST model!")

print("\nTraining complete!")
print("Best Val Accuracy =", best_acc)
