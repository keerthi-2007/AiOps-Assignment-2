
from fastapi import FastAPI
from pydantic import BaseModel
import joblib

app = FastAPI()

# Load model at application startup
model = joblib.load("model.joblib")


class PredictionRequest(BaseModel):
    text: str


@app.post("/predict")
def predict(request: PredictionRequest):
    prediction = model.predict([request.text])[0]
    return {"label": prediction}


@app.get("/healthz")
def health_check():
    return {"status": "ok"}
