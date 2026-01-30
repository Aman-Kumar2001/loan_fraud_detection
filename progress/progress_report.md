<h1> Project Progress Report — Loan Fraud Detection System </h1>

<h3>Objective</h3>

Build an end-to-end, real-world fraud detection system covering data ingestion, feature engineering, modeling, evaluation, and tuning, with deployment readiness.

Work Completed So Far

1. Data Engineering & Ingestion

Selected a realistic, highly imbalanced fraud dataset (PaySim).

Designed a normalized PostgreSQL schema for transactions, labels, and features.

Built a Python ingestion pipeline to load large CSV data into SQL safely.

Validated data integrity (row counts, label alignment, sanity checks).

2. Feature Engineering (SQL-based)

Created behavioral, time-aware features using SQL window functions:

Sender transaction count (last 24 hours)

Sender average transaction amount (last 24 hours)

Time since last transaction

Ensured no data leakage by using only past/current data.

3. Baseline Modeling

Trained a Logistic Regression baseline directly from SQL features.

Observed expected failure on imbalanced data (low fraud recall).

Used this to justify moving to more expressive models.

4. Improved Modeling

Implemented a Random Forest classifier with class imbalance handling.

Achieved strong initial results:

Fraud recall ≈ 0.78

Fraud precision ≈ 0.50

Using only 3–4 interpretable features

5. Hyperparameter Tuning

Applied RandomizedSearchCV, optimizing for recall (not accuracy).

Identified a more stable configuration (min_samples_leaf, class weighting).

Understood cross-validation vs single-split behavior to avoid overfitting.
