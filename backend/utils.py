import time
import json

def make_response(predictions, products, profile):
    """
    predictions: dict with acne/skin_type/skin_tone
    products: list of product dicts
    profile: final applied profile (sensitive flag etc)
    """
    res = {
        "predictions": predictions,
        "profile": profile,
        "recommended_products": products,
        "generated_at": int(time.time())
    }
    return res
