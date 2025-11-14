import torch.nn as nn
import torchvision.models as models

def build_skin_tone_model(num_classes=6, pretrained=True):
    model = models.resnet50(pretrained=pretrained)
    in_f = model.fc.in_features
    model.fc = nn.Sequential(
        nn.Dropout(0.4),
        nn.Linear(in_f, 512),
        nn.ReLU(),
        nn.Dropout(0.3),
        nn.Linear(512, num_classes)
    )
    return model
