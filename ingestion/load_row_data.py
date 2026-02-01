import os
from dotenv import load_dotenv
import psycopg2
import pandas as pd
from psycopg2.extras import execute_values

load_dotenv()

conn = psycopg2.connect(
    host=os.getenv("DB_HOST"),
    database=os.getenv("DB_NAME"),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD")
)

cur = conn.cursor()
conn.autocommit = False

CSV_PATH = "data/raw/paysim.csv"
CHUNK_SIZE = 5000

print("Starting batch ingestion...")

for chunk in pd.read_csv(CSV_PATH, chunksize=CHUNK_SIZE):

    # -------------------------------
    # Insert transactions + RETURN ids
    # -------------------------------
    transactions_data = [
        (
            row.step,
            row.type,
            row.amount,
            row.nameOrig,
            row.nameDest,
            row.oldbalanceOrig,
            row.newbalanceOrig,
            row.oldbalanceDest,
            row.newbalanceDest
        )
        for row in chunk.itertuples(index=False)
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
            new_balance_receiver
        )
        VALUES %s
        RETURNING transaction_id
        """,
        transactions_data
    )

    transaction_ids = [row[0] for row in cur.fetchall()]

    # -------------------------------
    # Insert fraud labels using ids
    # -------------------------------
    fraud_data = [
        (
            tx_id,
            bool(row.isFraud),
            bool(row.isFlaggedFraud)
        )
        for tx_id, row in zip(transaction_ids, chunk.itertuples(index=False))
    ]


    execute_values(
        cur,
        """
        INSERT INTO fraud_labels (transaction_id, is_fraud, is_flagged)
        VALUES %s
        """,
        fraud_data
    )

    conn.commit()
    print(f"Inserted {len(chunk)} rows...")

cur.close()
conn.close()

print("✅ Full CSV ingestion completed successfully.")
