from sklearn.preprocessing import OrdinalEncoder, StandardScaler, LabelEncoder
from sklearn.impute import SimpleImputer
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline

def preprocessing(num_cols, ord_cols):

    num_pipe = Pipeline(steps=[("num_imputing", SimpleImputer(strategy="median")),
                               ("num_scaling", StandardScaler())])
    
    ord_pipe = Pipeline(steps=[("encoding", OrdinalEncoder(handle_unknown="use_encoded_value", unknown_value=-1))])
    
    trf = ColumnTransformer(transformers=[("num_process", num_pipe, num_cols),
                                          ("ord_process", ord_pipe, ord_cols)],
                                          remainder="drop")
    
    return trf
