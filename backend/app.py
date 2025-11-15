from fastapi import FastAPI, UploadFile
import shutil
import os
from recommender import predict_all


app = FastAPI()

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)


@app.post("/predict")
async def analyze_image(img: UploadFile):
    img_path = os.path.join(UPLOAD_DIR, img.filename)

    with open(img_path, "wb") as f:
        shutil.copyfileobj(img.file, f)

    result = predict_all(img_path)

    return {
        "message": "Prediction successful",
        "result": result
    }
