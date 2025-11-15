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
Create a personalised AM and PM skincare routine in ONLY valid JSON format.

User Profile:
- Acne severity: {acne_label}
- Skin type: {type_label}
- Fitzpatrick skin tone: {tone_label}
- Sensitive skin: {sens_text}
- Budget: {budget_text}

Rules:
- Output ONLY JSON. No extra text.
- AM routine: 3–6 steps.
- PM routine: 4–6 steps.
- Include price ranges in INR.
- If sensitive = Yes → no fragrances, no harsh exfoliants.
- Respect budget if provided.
- Use real products commonly available in India OR global equivalents.

JSON Format:
{{
  "profile": {{
    "acne": "",
    "skin_type": "",
    "skin_tone": "",
    "sensitive": true/false,
    "budget_inr": number
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
