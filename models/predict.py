import joblib
import pandas as pd

artifact = joblib.load("artifact/fraud_model.pkl")

model = artifact["model"]
threshold = artifact["threshold"]

def predict_fraud(data):
    df = pd.DataFrame([data])
    prob = model.predict_proba(df)[0,1]
    pred = (prob >= threshold).astype(int)

    if pred == 0:
        msg = "This transaction may not be a fraud."
    else:
        msg = "This transaction is probably a fraud."

    return {"probability": float(prob),
        "prediction": pred,
        "message": msg}