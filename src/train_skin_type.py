import torch
import torch.nn as nn
import torch.optim as optim
from torch.optim.lr_scheduler import CosineAnnealingLR
from torch.utils.data import DataLoader
from sklearn.metrics import accuracy_score
import os

from dataset import ImageFolderDataset, get_transforms
from model_skin_type import build_skin_type_model


def main():
    DATA_DIR = "data/skin_type/Oily-Dry-Skin-Types"

    device = "cuda" if torch.cuda.is_available() else "cpu"
    print("Using:", device)

    print("Loading datasets...")
    train_ds = ImageFolderDataset(DATA_DIR, split="train", transform=get_transforms(True))
    val_ds = ImageFolderDataset(DATA_DIR, split="valid", transform=get_transforms(False))

    print("Train samples:", len(train_ds))
    print("Val samples:", len(val_ds))

    train_loader = DataLoader(train_ds, batch_size=32, shuffle=True, num_workers=0)
    val_loader = DataLoader(val_ds, batch_size=32, shuffle=False, num_workers=0)

    print("Loading EfficientNet-B0...")
    model = build_skin_type_model(num_classes=3).to(device)

    opt = optim.Adam(model.parameters(), lr=1e-4)
    scheduler = CosineAnnealingLR(opt, T_max=10)
    crit = nn.CrossEntropyLoss()

    best_acc = 0
    epochs = 12

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

        # Validation
        model.eval()
        preds_list, labels_list = [], []
        with torch.no_grad():
            for imgs, labels in val_loader:
                imgs = imgs.to(device)
                out = model(imgs)
                preds_list.extend(out.argmax(1).cpu())
                labels_list.extend(labels)

        acc = accuracy_score(labels_list, preds_list)
        print(f"Val Acc = {acc:.4f}")

        scheduler.step()

        if acc > best_acc:
            best_acc = acc
            os.makedirs("models", exist_ok=True)
            torch.save(model.state_dict(), "models/skin_type.pth")
            print("Saved BEST model!")

    print("\nTraining complete!")


if __name__ == "__main__":
    main()
