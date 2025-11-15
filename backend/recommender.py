import os
import json
import torch
from groq import Groq
from dotenv import load_dotenv

from ml_models import ACNE_MODEL, SKIN_TYPE_MODEL, SKIN_TONE_MODEL, DEVICE
from preprocess import preprocess_image
from utils import map_acne, map_skin_type, map_skin_tone

# Load environment variables
load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))


def predict_all(img_path):
    img = preprocess_image(img_path).to(DEVICE)

    acne_pred = ACNE_MODEL(img).argmax(1).item()
    type_pred = SKIN_TYPE_MODEL(img).argmax(1).item()
    tone_pred = SKIN_TONE_MODEL(img).argmax(1).item()

    return {
        "acne_level": acne_pred,
        "skin_type": type_pred,
        "skin_tone": tone_pred
    }


def llm_recommend(acne_label, type_label, tone_label, sensitive, budget):
    """
    Ask LLM to recommend products across markets (India, K-Beauty, US)
    while respecting budget and sensitivity.
    budget: integer INR (0 = no limit)
    """
    sens_text = "Yes" if sensitive else "No"
    budget_text = "No budget limit" if (not budget or budget <= 0) else f"Up to ₹{budget}"

    # Allowed brands: Indian + K-beauty + US (model should prefer in-market availability)
    prompt = f"""
You are a certified dermatologist + product recommender. Output EXACT JSON array only (no extra commentary).

Task:
Recommend EXACTLY 8 real skincare products appropriate for the user profile below. Provide products across three markets where possible: (1) India brands, (2) K-beauty brands, (3) US/global brands. Prioritize Indian availability if budget is modest.

Profile:
- Acne severity: {acne_label}
- Skin type: {type_label}
- Fitzpatrick skin tone: {tone_label}
- Sensitive skin: {sens_text}
- Budget: {budget_text}

Rules (VERY IMPORTANT):
1. Return exactly a JSON array of 8 objects. Example format:
[
  {{
    "name": "Product name",
    "brand": "Brand",
    "market": "india|k-beauty|us",
    "price_in_inr": "₹X - ₹Y",
    "primary_ingredient": "salicylic acid / niacinamide / hyaluronic acid / retinol / azelaic acid / etc.",
    "why_recommended": "1-2 short sentences explaining suitability for this profile"
  }}
]

2. Ensure products are REAL (available in India or globally). Prefer products that are actually sold in Indian stores or on Amazon.in / Nykaa / chemist sites.
3. If sensitive = Yes, avoid recommending fragranced products and high concentration retinoids; prefer gentle formulations.
4. If a budget is provided (e.g. ₹500), only include products that reasonably fit within that budget or include low-cost alternatives in the array. If budget is "no limit" choose a mix of budget + premium.
5. For K-beauty items, mention market 'k-beauty'; for Indian brands use 'india'; for US/global use 'us'.
6. Price ranges should be in INR. If exact INR price unknown, provide an approximate INR range.
7. Output JSON only. No prose, no lists, no commentary.

Now produce the JSON array (8 items).
"""

    # call Groq
    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.2
    )

    return response.choices[0].message.content


def recommend_products(acne_level, skin_type, skin_tone, sensitive=False, budget=0):
    acne_label = map_acne(acne_level)
    type_label = map_skin_type(skin_type)
    tone_label = map_skin_tone(skin_tone)

    raw = llm_recommend(acne_label, type_label, tone_label, sensitive, budget)

    # Try to parse JSON, fallback to raw string
    try:
        parsed = json.loads(raw)
        return {
            "skin_profile": {
                "acne": acne_label,
                "skin_type": type_label,
                "skin_tone": tone_label,
                "sensitive": sensitive,
                "budget": budget
            },
            "recommendations": parsed
        }
    except Exception:
        # If LLM returns some extra text or slightly invalid JSON, return raw with note
        return {
            "skin_profile": {
                "acne": acne_label,
                "skin_type": type_label,
                "skin_tone": tone_label,
                "sensitive": sensitive,
                "budget": budget
            },
            "recommendations": raw,
            "warning": "Could not parse LLM JSON automatically — returned raw string. You can inspect and adjust prompt or parse manually."
        }
