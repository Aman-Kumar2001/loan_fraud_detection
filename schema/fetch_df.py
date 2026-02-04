import pandas as pd
import psycopg2
from dotenv import load_dotenv
import os

load_dotenv()

def fetch_df():

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
        f.is_transfer_or_cashout,

        /* Labels */
        COALESCE(l.is_flagged, FALSE) AS is_flagged,
        COALESCE(l.is_fraud, FALSE)   AS is_fraud

    FROM transaction_features f
    LEFT JOIN fraud_labels l
    ON f.transaction_id = l.transaction_id;

    """

    df = pd.read_sql(query, conn)
    conn.close()

    return df