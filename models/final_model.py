from sklearn.ensemble import RandomForestClassifier
from schema.fetch_df import fetch_df
import joblib

df = fetch_df()

df["time_since_last_txn"] = df["time_since_last_txn"].fillna(999)

X = df.drop(columns=["is_fraud"])
y = df["is_fraud"]


rf_model = RandomForestClassifier(n_estimators = 100, n_jobs=-1, class_weight="balanced", random_state=42)

rf_model.fit(X, y)

artifact = {
    "model": rf_model,
    "threshold": 0.42,
    "features": list(X.columns)
}

model_path = "artifacts/fraud_model.pkl"

joblib.dump(artifact, model_path)


