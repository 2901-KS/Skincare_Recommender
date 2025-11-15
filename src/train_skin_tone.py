import os
import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader
from dataset import ImageFolderDataset, get_transforms
from model_skin_tone import build_skin_tone_model
from sklearn.metrics import accuracy_score
import multiprocessing
multiprocessing.freeze_support()

def main():
    device = "cuda" if torch.cuda.is_available() else "cpu"
    print(f"Using: {device}")

    DATA_DIR = "data/fitzpatrick"

    print("Loading datasets...")
    train_ds = ImageFolderDataset(DATA_DIR, split="train", transform=get_transforms(True))
    val_ds   = ImageFolderDataset(DATA_DIR, split="val",   transform=get_transforms(False))

    print(f"Train samples: {len(train_ds)}")
    print(f"Val samples  : {len(val_ds)}")

    train_loader = DataLoader(train_ds, batch_size=32, shuffle=True, num_workers=0)
    val_loader   = DataLoader(val_ds, batch_size=32, shuffle=False, num_workers=0)

    print("Loading ResNet18...")
    model = build_skin_tone_model(num_classes=6, pretrained=True).to(device)

    opt = optim.Adam(model.parameters(), lr=1e-4)
    crit = nn.CrossEntropyLoss()

    best_acc = 0
    epochs = 10

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

        # --- validation ---
        model.eval()
        preds_list, labels_list = [], []
        with torch.no_grad():
            for imgs, labels in val_loader:
                imgs = imgs.to(device)
                out = model(imgs)
                preds_list.extend(out.argmax(1).cpu().tolist())
                labels_list.extend(labels.tolist())

        acc = accuracy_score(labels_list, preds_list)
        print(f"Val Acc = {acc:.4f}")

        if acc > best_acc:
            best_acc = acc
            os.makedirs("models", exist_ok=True)
            torch.save(model.state_dict(), "models/skin_tone.pth")
            print("Saved BEST model!")

if __name__ == "__main__":
    main()
