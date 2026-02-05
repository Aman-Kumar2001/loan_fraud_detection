from fastapi import FastAPI
import pandas as pd
from fastapi.responses import JSONResponse
from models.predict import predict_fraud
from schema.pydantic_model import Transaction

app = FastAPI()

@app.get("/")
def home():
    return {"message" : "API is running properly."}

@app.get("/health")
def health():
    return { "Status" : "OK"}

@app.post("/predict")
def predict(data : Transaction):
    input = data.model_dump()
    input_df = pd.DataFrame([input])

    pred = predict_fraud(input_df)

    return JSONResponse(status_code=200, content=pred)