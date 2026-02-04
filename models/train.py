import pandas as pd
import numpy as np
import psycopg2
from dotenv import load_dotenv
import os

from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report
from imblearn.over_sampling import SMOTE

load_dotenv()

conn = psycopg2.connect(
    host=os.getenv("DB_HOST"),
    database=os.getenv("DB_NAME"),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD")
)

query = """
SELECT
    f.sender_txn_count_24h,
    f.sender_txn_count_1h,
    f.sender_avg_amount_24h,
    f.time_since_last_txn,
    f.receiver_txn_count_24h,
    f.amount_to_sender_avg_ratio,
    f.balance_drain_ratio,
    f.amount_change_ratio,
    f.is_time_compressed,
    f.is_new_sender,

    /* Labels */
    COALESCE(l.is_flagged, FALSE) AS is_flagged,
    COALESCE(l.is_fraud, FALSE)   AS is_fraud

FROM transaction_features f
LEFT JOIN fraud_labels l
ON f.transaction_id = l.transaction_id;

"""

df = pd.read_sql(query, conn)
conn.close()


# Handle NULLs 
df["time_since_last_txn"] = df["time_since_last_txn"].fillna(999)


X = df.drop(columns=["is_fraud"])
y = df["is_fraud"]
print(X.shape)
print(y.value_counts())


X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

smote = SMOTE(random_state=42)
X_train_res, y_train_res = smote.fit_resample(X_train, y_train)

print(X_train_res.shape)

model = LogisticRegression( class_weight='balanced', max_iter=1000, random_state=42)
model.fit(X_train_res, y_train_res)

y_prob = model.predict_proba(X_test)[:,1]

thresholds = [0.3, 0.4, 0.5]
for val in thresholds:
    y_pred = (y_prob > val).astype(int)
    print("Classification report for :", val, "\n" )
    print(classification_report(y_test, y_pred))
