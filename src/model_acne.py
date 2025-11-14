import torch.nn as nn
import torchvision.models as models

def build_acne_model(num_classes=2, pretrained=True):
    model = models.resnet34(pretrained=pretrained)
    in_f = model.fc.in_features
    model.fc = nn.Sequential(
        nn.Dropout(0.4),
        nn.Linear(in_f, 256),
        nn.ReLU(),
        nn.Dropout(0.3),
        nn.Linear(256, num_classes)
    )
    return model
