import os
import json
from groq import Groq
from dotenv import load_dotenv
from utils import map_acne, map_skin_type, map_skin_tone

load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))


# ---------------------------------
# 1. INGREDIENT SAFETY CHECK
# ---------------------------------
def ingredient_check(ingredients, acne_level, skin_type, skin_tone, sensitive):

    acne_label = map_acne(acne_level)
    type_label = map_skin_type(skin_type)
    tone_label = map_skin_tone(skin_tone)
    sens = "Yes" if sensitive else "No"

    prompt = f"""
You are a professional cosmetic chemist + dermatologist.

User Skin Profile:
- Acne Level: {acne_label}
- Skin Type: {type_label}
- Fitzpatrick Tone: {tone_label}
- Sensitive Skin: {sens}

Ingredient List to Analyze:
{ingredients}

TASK:
1. Identify harmful or irritating ingredients for THIS skin profile.
2. Identify beneficial ingredients.
3. Tell if the product is SAFE or NOT SAFE.
4. Provide a short explanation.
5. Output EXACT JSON format:

{{
  "safe": true/false,
  "good_ingredients": [],
  "irritants": [],
  "verdict": "",
  "reason": ""
}}
"""

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.2
    )

    raw = response.choices[0].message.content

    try:
        return json.loads(raw)
    except:
        return {"raw": raw, "warning": "JSON parsing failed"}



# ---------------------------------
# 2. PRODUCT COMPARISON ENGINE
# ---------------------------------
def compare_products(p1, p2, acne_level, skin_type, skin_tone, sensitive):

    acne_label = map_acne(acne_level)
    type_label = map_skin_type(skin_type)
    tone_label = map_skin_tone(skin_tone)
    sens = "Yes" if sensitive else "No"

    prompt = f"""
Compare these two skincare products for the user's skin:

Product 1: {p1}
Product 2: {p2}

User Skin Profile:
- Acne Level: {acne_label}
- Skin Type: {type_label}
- Fitzpatrick Tone: {tone_label}
- Sensitive Skin: {sens}

TASK:
1. Which product is better & why?
2. Pros and cons of each.
3. Which one to avoid.
4. Final recommendation.

Output ONLY JSON:

{{
  "better_product": "",
  "why_better": "",
  "product1_pros": [],
  "product1_cons": [],
  "product2_pros": [],
  "product2_cons": [],
  "final_recommendation": ""
}}
"""

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.25
    )

    raw = response.choices[0].message.content

    try:
        return json.loads(raw)
    except:
        return {"raw": raw, "warning": "JSON parsing failed"}
