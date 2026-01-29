import pandas as pd
import psycopg2
from dotenv import load_dotenv
import os

from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report

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
    f.sender_avg_amount_24h,
    f.time_since_last_txn,
    l.is_fraud
FROM transaction_features f
JOIN fraud_labels l
ON f.transaction_id = l.transaction_id;
"""

df = pd.read_sql(query, conn)
conn.close()


# Handle NULLs 
df["time_since_last_txn"] = df["time_since_last_txn"].fillna(999)

X = df.drop(columns=["is_fraud"])
y = df["is_fraud"]


X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

model = LogisticRegression(class_weight="balanced", max_iter=1000)
model.fit(X_train, y_train)

y_pred = model.predict(X_test)

print(classification_report(y_test, y_pred))
