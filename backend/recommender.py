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
You are a certified dermatologist, cosmetic chemist, and global skincare reviewer.
Your job is to recommend REAL skincare products across Indian, K-beauty, and US/global markets.

🔥 OUTPUT REQUIREMENT:
Return ONLY a valid JSON array of EXACTLY 8 product objects. No text outside JSON.

──────────────────────────────────
USER PROFILE
──────────────────────────────────
Acne severity: {acne_label}
Skin type: {type_label}
Fitzpatrick skin tone: {tone_label}
Sensitive skin: {"Yes" if sensitive else "No"}

──────────────────────────────────
STRICT RULES (FOLLOW 100%)
──────────────────────────────────
1. Output ONLY valid JSON array:
[
  {{
    "name": "",
    "brand": "",
    "market": "india | k-beauty | us",
    "price_in_inr": "",
    "primary_ingredient": "",
    "why_recommended": ""
  }},
  ...
]

2. **NO repetition**:
   - No product name repeats.
   - No brand repeats.
   - All 8 products must be unique.

3. Product sources must be **REAL**:
   - Products should exist in India, Korea, or USA/global markets.
   - No hallucinated products or imaginary variants.

4. Sensitive = Yes:
   - Avoid fragrance-heavy products.
   - Avoid essential oils, witch hazel, menthol, eucalyptus.
   - Prefer gentle formulations.

5. Acne rules:
   - Use either salicylic acid OR benzoyl peroxide in the entire 8 items, not both.
   - Niacinamide, azelaic acid, and zinc are allowed.
   - Avoid harsh peels unless acne is severe.

6. Skin tone safety:
   - Fitzpatrick III+ → avoid strong glycolic acid, high-strength retinoids, or peels.

7. Market tagging:
   - Indian brands → "india"
   - Korean brands → "k-beauty"
   - US/global brands → "us"

8. Explanation:
   - “why_recommended” must be 1–2 sentences, dermatologist tone.

──────────────────────────────────
IMPORTANT
──────────────────────────────────
- Ignore budget entirely.
- Focus on dermatologist-grade product quality and relevance.
- Keep JSON clean and parseable.

Now generate the JSON array of 8 products.
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