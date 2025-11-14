import os
import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader
from sklearn.metrics import accuracy_score
from dataset import ImageFolderDataset, get_transforms
from model_skin_tone import build_skin_tone_model

device = "cuda" if torch.cuda.is_available() else "cpu"
os.makedirs("models", exist_ok=True)

train_ds = ImageFolderDataset("data/fitzpatrick", split="train", transform=get_transforms(True))
val_ds   = ImageFolderDataset("data/fitzpatrick", split="val", transform=get_transforms(False))

train_loader = DataLoader(train_ds, batch_size=32, shuffle=True)
val_loader   = DataLoader(val_ds, batch_size=32, shuffle=False)

model = build_skin_tone_model().to(device)
opt = optim.Adam(model.parameters(), lr=1e-4)
crit = nn.CrossEntropyLoss()

best = 0

for epoch in range(12):
    model.train()
    for imgs, labels in train_loader:
        imgs, labels = imgs.to(device), labels.to(device)
        opt.zero_grad()
        out = model(imgs)
        loss = crit(out, labels)
        loss.backward()
        opt.step()

    # validation
    model.eval()
    preds, trues = [], []
    with torch.no_grad():
        for imgs, labels in val_loader:
            imgs = imgs.to(device)
            out = model(imgs)
            preds.extend(out.argmax(1).cpu().tolist())
            trues.extend(labels.tolist())

    acc = accuracy_score(trues, preds)
    print(f"Epoch {epoch+1} — Val Acc = {acc:.4f}")

    if acc > best:
        best = acc
        torch.save(model.state_dict(), "models/skin_tone.pth")
        print("Saved best model!")

print("Training complete.")
