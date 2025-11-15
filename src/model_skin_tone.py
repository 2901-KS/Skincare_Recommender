import torch.nn as nn
import torchvision.models as models

def build_skin_tone_model(num_classes=6, pretrained=True):
    # Use ResNet18 for fast CPU training
    model = models.resnet18(weights="IMAGENET1K_V1" if pretrained else None)

    in_f = model.fc.in_features
    model.fc = nn.Sequential(
        nn.Dropout(0.3),
        nn.Linear(in_f, 256),
        nn.ReLU(),
        nn.Dropout(0.2),
        nn.Linear(256, num_classes)
    )
    return model
