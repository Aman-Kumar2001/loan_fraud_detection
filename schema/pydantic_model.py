from pydantic import BaseModel, Field
from typing import Annotated

class Transaction(BaseModel):

    sender_txn_count_24h: Annotated[
        int,
        Field(..., ge=0, description="Number of transactions by sender in last 24 hours")
    ]

    sender_txn_count_1h: Annotated[
        int,
        Field(..., ge=0, description="Number of transactions by sender in last 1 hour")
    ]

    sender_avg_amount_24h: Annotated[
        float,
        Field(..., ge=0, description="Average transaction amount by sender in last 24 hours")
    ]

    time_since_last_txn: Annotated[
        int,
        Field(..., ge=0, description="Time since last transaction (in hours)")
    ]

    receiver_txn_count_24h: Annotated[
        int,
        Field(..., ge=0, description="Number of transactions by receiver in last 24 hours")
    ]

    amount_to_sender_avg_ratio: Annotated[
        float,
        Field(..., ge=0, description="Ratio of transaction amount to sender's average amount")
    ]

    balance_drain_ratio: Annotated[
        float,
        Field(..., ge=0, le=1, description="Ratio of transaction amount to sender's previous balance")
    ]

    amount_change_ratio: Annotated[
        float,
        Field(..., ge=0, description="Ratio of current transaction amount to previous transaction amount")
    ]

    # Categorical / ordinal features (0 or 1)
    is_time_compressed: Annotated[
        int,
        Field(..., ge=0, le=1, description="1 if transactions are time-compressed, else 0")
    ]

    is_new_sender: Annotated[
        int,
        Field(..., ge=0, le=1, description="1 if sender is new, else 0")
    ]

    is_transfer_or_cashout: Annotated[
        int,
        Field(..., ge=0, le=1, description="1 if transaction type is TRANSFER or CASH_OUT")
    ]

    is_flagged: Annotated[
        int,
        Field(..., ge=0, le=1, description="1 if sender was previously flagged")
    ]
