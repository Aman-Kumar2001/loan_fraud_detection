<h1> Business Problem </h1>

Financial institutions process millions of transactions daily. A small fraction are fraudulent, but missing these transactions causes direct financial loss. The goal is to detect potentially fraudulent transactions as early as possible while minimizing disruption to legitimate users.

<h3> Dataset </h3>

Source: PaySim (synthetic financial transaction dataset)

Size: ~6.3 million transactions

Fraud rate: ~0.13% (highly imbalanced)

<h3> Feature Engineering </h3>

Instead of using raw transaction data, behavioral features were engineered using SQL, such as:
-Number of transactions in last 1h / 24h
-Average transaction amount
-Time since last transaction
-Balance drain ratio
-Amount deviation ratios
-Flags for risky transaction types (TRANSFER / CASH_OUT)
-These features better capture fraud patterns over time.

<h3> Model </h3>

-Model: RandomForestClassifier
-Why Random Forest?
-Handles non-linear patterns
-Robust to noise
-Works well with engineered features

<h3> Preprocessing: </h3>

-Missing value imputation
-Standard scaling (numeric features)
-Ordinal encoding (categorical flags)

<h3> Handling Class Imbalance </h3>

-Class imbalance handled using:
-Class weighting
-Threshold tuning
-Focused on PR-AUC, not accuracy (accuracy is misleading in fraud problems).

<h3> Metrics and Performance </h3>

             precision  recall  f1-score   support

    False      1.00      1.00      1.00   1270881
    True       0.73      0.95      0.82      1643


-PR-AUC ≈ 0.92
-Strong recall with controlled false positives
-Model ranks risky transactions effectively rather than producing high absolute probabilities

<h3> API </h3>

-Built using FastAPI
-Accepts engineered features
-Returns fraud probability, risk level, and decision


<h3>  Deployment </h3>

-Dockerized using a slim Python image
-Ready for cloud deployment (Render / AWS)

<h3> Future Improvements </h3>

-Online feature computation using live SQL
-Probability calibration
