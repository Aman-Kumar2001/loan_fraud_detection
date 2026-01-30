from sklearn.model_selection import train_test_split, RandomizedSearchCV
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report
from schema.fetch_df import fetch_df


df = fetch_df()

df["time_since_last_txn"] = df["time_since_last_txn"].fillna(999)

X = df.drop(columns=["is_fraud"])
y = df["is_fraud"]


X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

rf_model = RandomForestClassifier(n_estimators = 100, max_depth=None, min_samples_leaf= 5, class_weight="balanced", random_state=42)



parameters = {
    "n_estimators" : [100, 200, 300, 500],
    "max_depth" : [None, 10, 20],
    "min_samples_leaf" : [1, 5, 10],
    "class_weight" : ["balanced", {0:1,1:5}]
}

# search = RandomizedSearchCV(
#     estimator=rf_model,
#     param_distributions=parameters, 
#     n_iter=10,
#     cv=5, 
#     scoring='recall',
#     n_jobs=-1,  
#     random_state=42)

# search.fit(X_train, y_train)

# print(search.best_score_)
# print(search.best_params_)

rf_model.fit(X_train, y_train)

pred = rf_model.predict(X_test)

print(classification_report(y_test, pred))
