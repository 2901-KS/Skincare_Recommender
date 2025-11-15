import torch.nn as nn
from torchvision.models import efficientnet_b0, EfficientNet_B0_Weights

def build_skin_type_model(num_classes=3):
    weights = EfficientNet_B0_Weights.IMAGENET1K_V1
    model = efficientnet_b0(weights=weights)

    in_f = model.classifier[1].in_features
    model.classifier = nn.Sequential(
        nn.Dropout(0.4),
        nn.Linear(in_f, num_classes)
    )
    return model
