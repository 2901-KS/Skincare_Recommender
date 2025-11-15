from fastapi import FastAPI, UploadFile, File, Form
import shutil
import os

from recommender import predict_all, recommend_products
from regimen import generate_regimen
from smart_ai import ingredient_check, compare_products  # NEW IMPORT

app = FastAPI()

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# -------------------------------
# 1. PREDICT + PRODUCT RECOMMENDER
# -------------------------------
@app.post("/predict")
async def predict(
    img: UploadFile = File(...),
    sensitive: bool = Form(False),
    budget: int = Form(0)
):
    try:
        temp_path = os.path.join(UPLOAD_DIR, img.filename)
        with open(temp_path, "wb") as f:
            shutil.copyfileobj(img.file, f)

        preds = predict_all(temp_path)
        preds["sensitive"] = sensitive

        recos = recommend_products(
            preds["acne_level"],
            preds["skin_type"],
            preds["skin_tone"],
            sensitive,
            budget
        )

        return {
            "message": "Prediction + AI Recommendations Successful",
            "predictions": preds,
            "recommendations": recos
        }

    except Exception as e:
        return {"error": str(e)}



# -------------------------------
# 2. AM/PM SKINCARE REGIMEN
# -------------------------------
@app.post("/regimen")
async def regimen(
    img: UploadFile = File(...),
    sensitive: bool = Form(False),
    budget: int = Form(0)
):
    try:
        temp_path = os.path.join(UPLOAD_DIR, img.filename)
        with open(temp_path, "wb") as f:
            shutil.copyfileobj(img.file, f)

        preds = predict_all(temp_path)

        routine = generate_regimen(
            preds["acne_level"],
            preds["skin_type"],
            preds["skin_tone"],
            sensitive,
            budget
        )

        return {
            "message": "Skincare Regimen Generated Successfully",
            "predictions": preds,
            "regimen": routine
        }

    except Exception as e:
        return {"error": str(e)}



# -------------------------------
# 3. INGREDIENT SAFETY CHECK
# -------------------------------
@app.post("/ingredient-check")
async def check_ingredients(
    ingredients: str = Form(...),
    acne_level: int = Form(...),
    skin_type: int = Form(...),
    skin_tone: int = Form(...),
    sensitive: bool = Form(False)
):
    try:
        result = ingredient_check(
            ingredients,
            acne_level,
            skin_type,
            skin_tone,
            sensitive
        )

        return {
            "message": "Ingredient Analysis Successful",
            "analysis": result
        }

    except Exception as e:
        return {"error": str(e)}



# -------------------------------
# 4. PRODUCT COMPARISON
# -------------------------------
@app.post("/compare-products")
async def compare(
    product1: str = Form(...),
    product2: str = Form(...),
    acne_level: int = Form(...),
    skin_type: int = Form(...),
    skin_tone: int = Form(...),
    sensitive: bool = Form(False)
):
    try:
        result = compare_products(
            product1,
            product2,
            acne_level,
            skin_type,
            skin_tone,
            sensitive
        )

        return {
            "message": "Product Comparison Successful",
            "comparison": result
        }

    except Exception as e:
        return {"error": str(e)}
