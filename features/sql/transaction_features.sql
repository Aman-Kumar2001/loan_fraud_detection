INSERT INTO transaction_features (
    transaction_id,
    sender_txn_count_24h,
    sender_avg_amount_24h,
    time_since_last_txn,
    receiver_txn_count_24h,
    is_new_sender,
    amount_to_sender_avg_ratio,
    balance_drain_ratio
)
SELECT
    t.transaction_id,

    /* Sender txn count (24h) */
    COUNT(*) OVER (
        PARTITION BY t.sender_id
        ORDER BY t.step
        RANGE BETWEEN 24 PRECEDING AND CURRENT ROW
    ) AS sender_txn_count_24h,

    /* Sender avg amount (24h) */
    AVG(t.amount) OVER (
        PARTITION BY t.sender_id
        ORDER BY t.step
        RANGE BETWEEN 24 PRECEDING AND CURRENT ROW
    ) AS sender_avg_amount_24h,

    /* Time since last txn */
    t.step - LAG(t.step) OVER (
        PARTITION BY t.sender_id
        ORDER BY t.step
    ) AS time_since_last_txn,

    /* Receiver txn count (24h) */
    COUNT(*) OVER (
        PARTITION BY t.receiver_id
        ORDER BY t.step
        RANGE BETWEEN 24 PRECEDING AND CURRENT ROW
    ) AS receiver_txn_count_24h,

    /* Is new sender */
    CASE
        WHEN COUNT(*) OVER (
            PARTITION BY t.sender_id
            ORDER BY t.step
            RANGE BETWEEN 24 PRECEDING AND CURRENT ROW
        ) = 1 THEN TRUE
        ELSE FALSE
    END AS is_new_sender,

    /* Amount deviation from sender avg */
    CASE
        WHEN AVG(t.amount) OVER (
            PARTITION BY t.sender_id
            ORDER BY t.step
            RANGE BETWEEN 24 PRECEDING AND CURRENT ROW
        ) = 0 THEN NULL
        ELSE t.amount /
             AVG(t.amount) OVER (
                 PARTITION BY t.sender_id
                 ORDER BY t.step
                 RANGE BETWEEN 24 PRECEDING AND CURRENT ROW
             )
    END AS amount_to_sender_avg_ratio,

    /* Balance drain ratio */
    CASE
        WHEN t.old_balance_sender = 0 THEN NULL
        ELSE t.amount / t.old_balance_sender
    END AS balance_drain_ratio

FROM transactions t;
