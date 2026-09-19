from fastapi import FastAPI
from pydantic import BaseModel
import joblib
app = FastAPI()
model = joblib.load("model.joblib")
VERSION = "v1"
class PredictionRequest(BaseModel):
    test:str

@app.post("/predict")
def predict(request: PredictionRequest):
    prediction = model.predict([request.text])[0]
    return {"label": prediction}

@app.get("/healthz")
def health_check():
    return {
        "status": "ok",
        "version": "v2"
    }
