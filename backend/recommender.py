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


def llm_recommend(acne_label, type_label, tone_label, sensitive):
    """
    Ask LLM to recommend products across markets (India, K-Beauty, US)
    WITHOUT budget constraints.
    """
    sens_text = "Yes" if sensitive else "No"

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
Sensitive skin: {sens_text}

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

3. Product sources must be REAL:
   - Products should exist in India, Korea, or global/US markets.
   - No hallucinated items.

4. Sensitive = Yes:
   - Avoid fragrance-heavy products.
   - Avoid essential oils, witch hazel, menthol, eucalyptus.
   - Prefer gentle formulations.

5. Acne rules:
   - Use either salicylic acid OR benzoyl peroxide across all products, not both.
   - Niacinamide, azelaic acid, and zinc are allowed.

6. Skin tone safety:
   - Fitzpatrick III+ → avoid strong glycolic acid, aggressive peels, or high-strength retinoids.

7. Market tag rules:
   - Indian brands → "india"
   - Korean brands → "k-beauty"
   - US/global → "us"

8. Explanation:
   - “why_recommended” must be 1–2 concise dermatologist sentences.

──────────────────────────────────
IMPORTANT
──────────────────────────────────
- IGNORE ALL BUDGET CONSTRAINTS.
- Focus only on dermatologist-grade quality and profile suitability.
- Keep JSON STRICT, CLEAN, and PARSEABLE.

Now generate the JSON array of 8 products.
"""

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.2
    )

    return response.choices[0].message.content


def recommend_products(acne_level, skin_type, skin_tone, sensitive=False, budget=0):
    """
    Wrapper for FastAPI — budget kept for backward compatibility but NOT USED.
    """
    acne_label = map_acne(acne_level)
    type_label = map_skin_type(skin_type)
    tone_label = map_skin_tone(skin_tone)

    raw = llm_recommend(acne_label, type_label, tone_label, sensitive)

    # Parse JSON safely
    try:
        parsed = json.loads(raw)
        return {
            "skin_profile": {
                "acne": acne_label,
                "skin_type": type_label,
                "skin_tone": tone_label,
                "sensitive": sensitive
            },
            "recommendations": parsed
        }
    except Exception:
        return {
            "skin_profile": {
                "acne": acne_label,
                "skin_type": type_label,
                "skin_tone": tone_label,
                "sensitive": sensitive
            },
            "recommendations": raw,
            "warning": "LLM returned non-JSON output. Inspect raw response."
        }
