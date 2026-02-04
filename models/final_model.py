from sklearn.ensemble import RandomForestClassifier
from schema.fetch_df import fetch_df
from preprocessing.preprocess import preprocessing
from sklearn.pipeline import Pipeline
import joblib

df = fetch_df()

df["time_since_last_txn"] = df["time_since_last_txn"].fillna(999)

X = df.drop(columns=["is_fraud"])
y = df["is_fraud"]

num_col = [
    'sender_txn_count_24h', 
    'sender_txn_count_1h', 
    'sender_avg_amount_24h', 
    'time_since_last_txn', 
    'receiver_txn_count_24h', 
    'amount_to_sender_avg_ratio', 
    'balance_drain_ratio', 
    'amount_change_ratio'
    ]

ord_col = [
    'is_time_compressed', 
    'is_new_sender', 
    'is_transfer_or_cashout', 
    'is_flagged'
    ]

preprocess_trf = preprocessing(num_col, ord_col)

rf_model = RandomForestClassifier(
    n_estimators = 300, 
    max_depth=None, 
    min_samples_leaf= 5,
    class_weight="balanced", 
    random_state=42)

rf_pipeline = Pipeline(steps=[("preprocess_trf", preprocess_trf),
                              ("rf_model", rf_model)])

rf_pipeline.fit(X, y)

artifact = {
    "model": rf_pipeline,
    "threshold": 0.3,
    "features": list(X.columns)
}

model_path = "artifacts/fraud_model.pkl"

joblib.dump(artifact, model_path)

print('Model artifact created...')


