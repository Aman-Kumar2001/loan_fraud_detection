from sklearn.ensemble import HistGradientBoostingClassifier
from sklearn.model_selection import train_test_split, RandomizedSearchCV
from sklearn.metrics import classification_report
from schema.fetch_df import fetch_df
from imblearn.over_sampling import SMOTE
from sklearn.preprocessing import StandardScaler


df = fetch_df()
print(df.shape)

df["time_since_last_txn"] = df["time_since_last_txn"].fillna(999)

X = df.drop(columns=["is_fraud"])
y = df["is_fraud"]

num_cols = ["sender_txn_count_24h", "sender_avg_amount_24h","sender_txn_count_1h","time_since_last_txn","sender_avg_amount_24h","receiver_txn_count_24h","amount_to_sender_avg_ratio","balance_drain_ratio","amount_change_ratio"]


X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

sc = StandardScaler()
X_train[num_cols] = sc.fit_transform(X_train[num_cols])
X_test[num_cols] = sc.transform(X_test[num_cols])


hgb_model = HistGradientBoostingClassifier( 
    learning_rate=0.1, 
    max_iter = 300, 
    min_samples_leaf=8,
    max_depth=10,
    random_state=42,
    class_weight='balanced'
    )

hgb_model.fit(X_train, y_train)

prob = hgb_model.predict_proba(X_test)[:,1]

for val in [0.25, 0.3, 0.4, 0.5]:
    pred = (prob >= val).astype(int)
    print(classification_report(y_test, pred))