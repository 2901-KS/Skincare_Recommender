import torch
from ml_models import ACNE_MODEL, SKIN_TYPE_MODEL, SKIN_TONE_MODEL, DEVICE
from preprocess import preprocess_image


def predict_all(img_path):
    img = preprocess_image(img_path).to(DEVICE)

    # Acne
    acne_pred = ACNE_MODEL(img).argmax(1).item()

    # Skin Type
    stype_pred = SKIN_TYPE_MODEL(img).argmax(1).item()

    # Skin Tone
    stone_pred = SKIN_TONE_MODEL(img).argmax(1).item()

    return {
        "acne_level": acne_pred,
        "skin_type": stype_pred,
        "skin_tone": stone_pred
    }
