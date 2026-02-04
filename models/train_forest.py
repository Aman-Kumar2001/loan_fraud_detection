from sklearn.model_selection import train_test_split, RandomizedSearchCV
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, average_precision_score
from schema.fetch_df import fetch_df
from imblearn.over_sampling import SMOTE


df = fetch_df()
print(df.shape)

df["time_since_last_txn"] = df["time_since_last_txn"].fillna(999)
df.fillna(0, inplace=True)

X = df.drop(columns=["is_fraud"])
y = df["is_fraud"]


X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

# smote = SMOTE(random_state=42)
# X_train_res, y_train_res = smote.fit_resample(X_train, y_train)

#rf_model = RandomForestClassifier(n_estimators = 200, n_jobs=-1, class_weight="balanced", random_state=42)
rf_model = RandomForestClassifier(n_estimators = 300, max_depth=None, min_samples_leaf= 5,  random_state=42)



# parameters = {
#     "n_estimators" : [200, 300, 500, 800],
#     "max_depth" : [10, 20, 25, 30],
#     "min_samples_leaf" : [1, 5, 10],
#     "class_weight" : ["balanced", {0:1,1:5}]
# }

# print("searching for best params")

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

print("Fitting the model...")

rf_model.fit(X_train, y_train)

prob = rf_model.predict_proba(X_test)[:,1]

for val in [0.05, 0.1, 0.2, 0.3, 0.4, 0.5]:
    pred = (prob >= val).astype(int)
    print(val)
    print(classification_report(y_test, pred))

print("PR-AUC:", average_precision_score(y_test, prob))
