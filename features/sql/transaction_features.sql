INSERT INTO transaction_features (
    transaction_id,
    sender_txn_count_24h,
    sender_txn_count_1h,
    sender_avg_amount_24h,
    time_since_last_txn,
    receiver_txn_count_24h,
    is_new_sender,
    amount_to_sender_avg_ratio,
    amount_change_ratio,
    balance_drain_ratio,
    is_time_compressed,
    is_transfer_or_cashout
)
SELECT
    t.transaction_id,

    /* Sender txn count (24h) */
    COUNT(*) OVER (
        PARTITION BY t.sender_id
        ORDER BY t.step
        RANGE BETWEEN 24 PRECEDING AND CURRENT ROW
    ) AS sender_txn_count_24h,

    /* Sender txn count (1h) */
    COUNT(*) OVER (
        PARTITION BY t.sender_id
        ORDER BY t.step
        RANGE BETWEEN 1 PRECEDING AND CURRENT ROW
    ) AS sender_txn_count_1h,

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

    /* Amount / sender avg (sentinel-safe) */
    CASE
        WHEN AVG(t.amount) OVER (
            PARTITION BY t.sender_id
            ORDER BY t.step
            RANGE BETWEEN 24 PRECEDING AND CURRENT ROW
        ) = 0 THEN -1
        ELSE t.amount /
             AVG(t.amount) OVER (
                 PARTITION BY t.sender_id
                 ORDER BY t.step
                 RANGE BETWEEN 24 PRECEDING AND CURRENT ROW
             )
    END AS amount_to_sender_avg_ratio,

    /* Amount change vs last txn (sentinel-safe) */
    CASE
        WHEN LAG(t.amount) OVER (
            PARTITION BY t.sender_id
            ORDER BY t.step
        ) IS NULL THEN -1
        WHEN LAG(t.amount) OVER (
            PARTITION BY t.sender_id
            ORDER BY t.step
        ) = 0 THEN -1
        ELSE t.amount /
             LAG(t.amount) OVER (
                 PARTITION BY t.sender_id
                 ORDER BY t.step
             )
    END AS amount_change_ratio,

    /* Balance drain ratio (sentinel-safe) */
    CASE
        WHEN t.old_balance_sender IS NULL THEN -1
        WHEN t.old_balance_sender = 0 THEN -1
        ELSE t.amount / t.old_balance_sender
    END AS balance_drain_ratio,

    /* Time compression (burst indicator) */
    CASE
        WHEN (t.step - LAG(t.step) OVER (
            PARTITION BY t.sender_id
            ORDER BY t.step
        )) <= 1 THEN TRUE
        ELSE FALSE
    END AS is_time_compressed,

    /* Transaction type prior */
    CASE
        WHEN t.transaction_type IN ('TRANSFER', 'CASH_OUT') THEN TRUE
        ELSE FALSE
    END AS is_transfer_or_cashout

FROM transactions t;
