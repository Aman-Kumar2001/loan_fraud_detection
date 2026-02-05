import joblib


artifact = joblib.load("artifacts/fraud_model.pkl")

model = artifact["model"]
threshold = artifact["threshold"]   


def predict_fraud(df):
    """
    Predict fraud risk for a single transaction (engineered features).
    """

    # Predict probability
    prob = model.predict_proba(df)[0, 1]
    prob = float(prob)  # JSON-safe

    # Risk bands 
    if prob >= 0.30:
        risk_level = "HIGH"
        fraud_prediction = 1
        message = "High risk of fraud. Immediate action recommended."
    elif prob >= 0.10:
        risk_level = "MEDIUM"
        fraud_prediction = 1   # still flag for review
        message = "Moderate fraud risk. Manual review suggested."
    else:
        risk_level = "LOW"
        fraud_prediction = 0
        message = "Low fraud risk."

    return {
        "fraud_probability": round(prob, 4),
        "fraud_prediction": int(fraud_prediction),
        "risk_level": risk_level,
        "message": message
    }
