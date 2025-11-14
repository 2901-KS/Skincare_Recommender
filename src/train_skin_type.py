import os
import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader
from torchvision import datasets, transforms
from sklearn.metrics import accuracy_score

from model_skin_type import build_skin_type_model

device = "cuda" if torch.cuda.is_available() else "cpu"

# Dataset path
DATA_DIR = "data/skin_type/Oily-Dry-Skin-Types"

# Transforms
train_tf = transforms.Compose([
    transforms.Resize((224,224)),
    transforms.RandomHorizontalFlip(),
    transforms.RandomRotation(10),
    transforms.ToTensor(),
    transforms.Normalize([0.485, 0.456, 0.406],
                         [0.229, 0.224, 0.225])
])

val_tf = transforms.Compose([
    transforms.Resize((224,224)),
    transforms.ToTensor(),
    transforms.Normalize([0.485, 0.456, 0.406],
                         [0.229, 0.224, 0.225])
])

# Datasets
train_ds = datasets.ImageFolder(os.path.join(DATA_DIR, "train"), transform=train_tf)
val_ds   = datasets.ImageFolder(os.path.join(DATA_DIR, "valid"), transform=val_tf)

train_loader = DataLoader(train_ds, batch_size=16, shuffle=True)
val_loader   = DataLoader(val_ds, batch_size=16, shuffle=False)

# Model
model = build_skin_type_model(num_classes=3).to(device)
opt = optim.Adam(model.parameters(), lr=1e-4)
crit = nn.CrossEntropyLoss()

best = 0

print("Training on:", device)

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

    # Validation
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

    # Save best
    if acc > best:
        best = acc
        os.makedirs("models", exist_ok=True)
        torch.save(model.state_dict(), "models/skin_type.pth")
        print("Saved best model!")
