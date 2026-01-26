CREATE TABLE transactions (
    transaction_id BIGSERIAL PRIMARY KEY,
    step INTEGER NOT NULL,
    transaction_type VARCHAR(20) NOT NULL,
    amount NUMERIC(14, 2) NOT NULL,
    sender_id VARCHAR(50) NOT NULL,
    receiver_id VARCHAR(50) NOT NULL,
    old_balance_sender NUMERIC(14, 2),
    new_balance_sender NUMERIC(14, 2),
    old_balance_receiver NUMERIC(14, 2),
    new_balance_receiver NUMERIC(14, 2),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);


CREATE TABLE fraud_labels (
    transaction_id BIGINT PRIMARY KEY,
    is_fraud BOOLEAN,
    is_flagged BOOLEAN,
    labeled_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (transaction_id) REFERENCES transactions(transaction_id)
);


CREATE TABLE transaction_features (
    transaction_id BIGINT PRIMARY KEY,
    sender_txn_count_1h INTEGER,
    sender_txn_count_24h INTEGER,
    sender_avg_amount_24h NUMERIC(14, 2),
    time_since_last_txn INTEGER,
    FOREIGN KEY (transaction_id) REFERENCES transactions(transaction_id)
);