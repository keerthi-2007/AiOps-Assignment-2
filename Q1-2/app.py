
from fastapi import FastAPI
from pydantic import BaseModel
import joblib
import redis
app = FastAPI()
model = joblib.load("model.joblib")
cache = redis.Redis(host = "cache", port = 6379, decode_responses=True)

class PredictionRequest(BaseModel):
    text:str

@app.post("/predict")
def predict(request: PredictionRequest):
    text = request.text
    cached_label = cache.get(text)
    if cached_label is not None:
        print("CACHE HIT")
        return {"label": cached_label}

    print("CACHE MISS")
    prediction = model.predict([text])[0]
    cache.setex(text, 60, prediction)
    return {"label": prediction}

@app.get("/healthz")
def health_check():
    return {"status" : "ok"}
