from xgboost import XGBClassifier
from sklearn.metrics import classification_report, average_precision_score
from sklearn.model_selection import train_test_split, RandomizedSearchCV
from schema.fetch_df import fetch_df


df = fetch_df()

df["time_since_last_txn"] = df["time_since_last_txn"].fillna(999)

X = df.drop(columns=["is_fraud"])
y = df["is_fraud"]


X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

counts = y_train.value_counts()

xgb = XGBClassifier(
    n_estimators=300,
    max_depth=4,
    learning_rate=0.05,
    subsample=0.8,
    colsample_bytree=0.8,
    scale_pos_weight = 1,
    objective="binary:logistic",
    eval_metric="logloss",
    random_state=42,
    n_jobs=-1
)

xgb.fit(X_train, y_train)

y_prob = xgb.predict_proba(X_test)[:, 1]

for t in [0.05, 0.1, 0.2, 0.3, 0.4, 0.5]:
    y_pred = (y_prob >= t).astype(int)
    print(f"\nThreshold = {t}")
    print(classification_report(y_test, y_pred, digits=3))

print("PR-AUC:", average_precision_score(y_test, y_prob))
