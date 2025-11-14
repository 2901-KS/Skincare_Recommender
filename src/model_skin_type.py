import torch.nn as nn
from torchvision import models

def build_skin_type_model(num_classes=3):
    model = models.resnet18(weights=models.ResNet18_Weights.DEFAULT)
    in_feats = model.fc.in_features
    model.fc = nn.Linear(in_feats, num_classes)
    return model
