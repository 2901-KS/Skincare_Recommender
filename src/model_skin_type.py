import torch.nn as nn
import torchvision.models as models

def build_skin_type_model(num_classes=3, pretrained=True):
    model = models.mobilenet_v2(pretrained=pretrained)
    in_f = model.classifier[1].in_features
    model.classifier = nn.Sequential(
        nn.Dropout(0.3),
        nn.Linear(in_f, 256),
        nn.ReLU(),
        nn.Dropout(0.2),
        nn.Linear(256, num_classes)
    )
    return model
