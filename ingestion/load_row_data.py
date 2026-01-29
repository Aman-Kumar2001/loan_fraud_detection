import os
from dotenv import load_dotenv
import psycopg2
import pandas as pd

load_dotenv()

conn = psycopg2.connect(
    host=os.getenv("DB_HOST"),
    database=os.getenv("DB_NAME"),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD")
)

cur = conn.cursor()

# Reading a Small sample first
df = pd.read_csv("data/raw/paysim.csv", nrows=100000)

# Looping over rows
for _, row in df.iterrows():
    cur.execute(
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
        VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)
        """,
        (
            row["step"],
            row["type"],
            row["amount"],
            row["nameOrig"],
            row["nameDest"],
            row["oldbalanceOrig"],
            row["newbalanceOrig"],
            row["oldbalanceDest"],
            row["newbalanceDest"]
        )
    )

    cur.execute(
        """
        INSERT INTO fraud_labels (transaction_id, is_fraud, is_flagged)
        VALUES (currval('transactions_transaction_id_seq'), %s, %s)
        """,
        (bool(row["isFraud"]), bool(row["isFlaggedFraud"]))
    )

# Saving changes
conn.commit()

cur.close()
conn.close()
