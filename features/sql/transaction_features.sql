INSERT INTO transaction_features (
    transaction_id,
    sender_txn_count_24h,
    sender_avg_amount_24h,
    time_since_last_txn
)
SELECT
    t.transaction_id,

    -- count transactions by sender in last 24 steps
    COUNT(*) OVER (
        PARTITION BY t.sender_id
        ORDER BY t.step
        RANGE BETWEEN 24 PRECEDING AND CURRENT ROW
    ) AS sender_txn_count_24h,

    -- average amount by sender in last 24 steps
    AVG(t.amount) OVER (
        PARTITION BY t.sender_id
        ORDER BY t.step
        RANGE BETWEEN 24 PRECEDING AND CURRENT ROW
    ) AS sender_avg_amount_24h,

    -- time since previous transaction
    t.step - LAG(t.step) OVER (
        PARTITION BY t.sender_id
        ORDER BY t.step
    ) AS time_since_last_txn

FROM transactions t;
