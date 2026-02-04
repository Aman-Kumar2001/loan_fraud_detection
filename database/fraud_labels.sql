CREATE TABLE fraud_labels AS
SELECT
    transaction_id,
    (is_fraud_raw = 1)   AS is_fraud,
    (is_flagged_raw = 1) AS is_flagged,
    CURRENT_TIMESTAMP    AS labeled_at
FROM transactions;


ALTER TABLE fraud_labels
ADD PRIMARY KEY (transaction_id);

ALTER TABLE fraud_labels
ADD CONSTRAINT fraud_labels_transaction_id_fkey
FOREIGN KEY (transaction_id)
REFERENCES transactions(transaction_id);
