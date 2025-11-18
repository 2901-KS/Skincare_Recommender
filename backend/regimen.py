import os
import json
from groq import Groq
from dotenv import load_dotenv

from utils import map_acne, map_skin_type, map_skin_tone

load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))


def generate_regimen(acne_level, skin_type, skin_tone, sensitive=False, budget=0):
    acne_label = map_acne(acne_level)
    type_label = map_skin_type(skin_type)
    tone_label = map_skin_tone(skin_tone)
    sens_text = "Yes" if sensitive else "No"
    budget_text = "No budget limit" if (not budget or budget <= 0) else f"Up to ₹{budget}"

    prompt = f"""
You are a senior dermatologist and cosmetic chemist.  
You MUST produce a personalised AM + PM skincare routine using STRICT JSON ONLY.

────────────────────────────────────────────────
USER PROFILE
────────────────────────────────────────────────
Acne severity: {acne_label}
Skin type: {type_label}
Fitzpatrick skin tone: {tone_label}
Sensitive: {"Yes" if sensitive else "No"}
Budget: {budget_text}

────────────────────────────────────────────────
CRITICAL RULES — FOLLOW 100%
────────────────────────────────────────────────
1. OUTPUT MUST BE ONLY VALID JSON (NO comments, markdown, or text).
2. The regimen MUST stay strictly within the budget.
3. You MUST AVOID repeating the same brand more than **once** across the full routine.
4. You MUST AVOID recommending these same products repeatedly:
   - Cetaphil Gentle Cleanser
   - Cetaphil Moisturiser
   - Minimalist 2% Salicylic Acid
   - Dermaco Niacinamide
   - Dermaco Sunscreen
   (Use alternatives instead unless clinically unavoidable.)
5. You MUST rotate across different brands. Allowed brand groups:
   - Cleansers: Re’equil, Bioderma, COSRX, Sebamed, Simple, Aqualogica.
   - Sunscreen: Re’equil, Aqualogica, Fixderma, La Shield, UV Doux, Rivela.
   - Actives: Minimalist, Deconstruct, Plum, Dr. Sheth’s, Olay, L’Oreal.
   - Moisturizers: Simple, Bioderma, Neutrogena, Earth Rhythm, Dot & Key.
   - Budget options: Himalaya, Mamaearth (mild), Garnier, Pond’s (non-fragranced).
6. PRODUCT VARIETY:  
   - AM and PM must use **different products**, unless medically required.
7. Safe formulation rules (override everything):
   - Sensitive → NO fragrance, NO essential oils, NO witch hazel, NO harsh acids.
   - Acne → Allow salicylic acid OR benzoyl peroxide, never both together.
   - Fitzpatrick III+ → Avoid high-strength exfoliants & strong retinoids.
8. Step count must follow:
   - AM: 3–6 steps  
   - PM: 4–6 steps
9. EVERY step must contain:
   - step number
   - name
   - what_to_use (real product)
   - approx_price_in_inr (INR)
   - why (dermatologist explanation)
10. If budget is low → prioritize essential steps (Cleanser + Moisturizer + Sunscreen).

────────────────────────────────────────────────
JSON FORMAT — FOLLOW EXACTLY
────────────────────────────────────────────────
{{
  "profile": {{
    "acne": "{acne_label}",
    "skin_type": "{type_label}",
    "skin_tone": "{tone_label}",
    "sensitive": {str(sensitive).lower()},
    "budget_inr": {budget if budget else 0}
  }},
  "am_routine": [
    {{
      "step": 1,
      "name": "",
      "what_to_use": "",
      "why": "",
      "approx_price_in_inr": ""
    }}
  ],
  "pm_routine": [
    {{
      "step": 1,
      "name": "",
      "what_to_use": "",
      "why": "",
      "approx_price_in_inr": ""
    }}
  ],
  "suggested_ingredients": [],
  "avoid": [],
  "notes": []
}}

────────────────────────────────────────────────
IMPORTANT VERIFICATIONS (APPLY BEFORE FINALISING)
────────────────────────────────────────────────
- NO single product should appear twice.
- NO single brand should appear more than once OR twice max.
- NO Cetaphil unless medically necessary AND budget allows AND not used repeatedly.
- Total cost must respect budget strictly (sum of approx_price_in_inr must stay within budget).
"""



    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",   # NEW MODEL
        messages=[{"role": "user", "content": prompt}],
        temperature=0.25
    )

    raw = response.choices[0].message.content

    # Try parsing JSON
    try:
        return json.loads(raw)
    except:
        return {
            "warning": "LLM returned unstructured output. Inspect raw response.",
            "raw": raw
        }
