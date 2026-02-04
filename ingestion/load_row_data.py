import os
from dotenv import load_dotenv
import psycopg2
import pandas as pd
from psycopg2.extras import execute_values

# -------------------------------
# DB connection
# -------------------------------
load_dotenv()

conn = psycopg2.connect(
    host=os.getenv("DB_HOST"),
    database=os.getenv("DB_NAME"),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD")
)

cur = conn.cursor()
conn.autocommit = False   # IMPORTANT


CSV_PATH = "data/raw/paysim.csv"
CHUNK_SIZE = 5000

print("Starting full CSV ingestion...")

# Reading and injecting values in chunks
for chunk in pd.read_csv(CSV_PATH, chunksize=CHUNK_SIZE):

    # ---- Insert transactions ----
    transactions_data = [
        (
            int(r.step),
            r.type,
            float(r.amount),
            r.nameOrig,
            r.nameDest,
            float(r.oldbalanceOrig),
            float(r.newbalanceOrig),
            float(r.oldbalanceDest),
            float(r.newbalanceDest),
            int(r.isFraud),
            int(r.isFlaggedFraud)
        )
        for r in chunk.itertuples(index=False)
    ]

    execute_values(
        cur,
        """
        INSERT INTO transactions (
            step,
            transaction_type,
            amount,
            sender_id,
            receiver_id,
            old_balance_sender,
            new_balance_sender,
            old_balance_receiver,
            new_balance_receiver,
            is_fraud_raw,
            is_flagged_raw
        )
        VALUES %s
        RETURNING transaction_id
        """,
        transactions_data
    )

conn.commit()

cur.close()
conn.close()

print("Full CSV ingestion completed successfully.")
