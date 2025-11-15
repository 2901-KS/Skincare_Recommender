import torch
import os
import sys

# Make sure backend can import from src/
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC_DIR = os.path.join(BASE_DIR, "src")
sys.path.append(SRC_DIR)

from model_acne import build_acne_model
from model_skin_type import build_skin_type_model
from model_skin_tone import build_skin_tone_model

DEVICE = "cuda" if torch.cuda.is_available() else "cpu"


def load_models():
    """Load all trained models from ../models/ folder."""
    models_dir = os.path.join(BASE_DIR, "models")

    acne_path = os.path.join(models_dir, "acne.pth")
    skin_type_path = os.path.join(models_dir, "skin_type.pth")
    skin_tone_path = os.path.join(models_dir, "skin_tone.pth")

    print("\n🔄 Loading models...")

    # Acne model
    acne_model = build_acne_model(num_classes=4).to(DEVICE)
    acne_model.load_state_dict(torch.load(acne_path, map_location=DEVICE))
    acne_model.eval()
    print("✔ Acne model loaded")

    # Skin TYPE model
    stype_model = build_skin_type_model(num_classes=3).to(DEVICE)
    stype_model.load_state_dict(torch.load(skin_type_path, map_location=DEVICE))
    stype_model.eval()
    print("✔ Skin Type model loaded")

    # Skin TONE (Fitzpatrick)
    stone_model = build_skin_tone_model(num_classes=6).to(DEVICE)
    stone_model.load_state_dict(torch.load(skin_tone_path, map_location=DEVICE))
    stone_model.eval()
    print("✔ Skin Tone (Fitzpatrick) model loaded")

    print("🎉 All models ready!\n")
    return acne_model, stype_model, stone_model


# GLOBAL MODELS FOR BACKEND
ACNE_MODEL, SKIN_TYPE_MODEL, SKIN_TONE_MODEL = load_models()
