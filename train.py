import pandas as pd
import xgboost as xgb
from sklearn.model_selection import TimeSeriesSplit
from helper_functions import *

# Load and clean dataset
df = pd.read_csv("AEP_hourly.csv", parse_dates=["Datetime"], index_col="Datetime")
df = df.query("AEP_MW > 9700 and AEP_MW < 24700").copy()

df = feature_extraction(df)
df = create_lag(df)

# Train/test split
tss = TimeSeriesSplit(n_splits=5, test_size=24 * 365, gap=24)
df = df.sort_index()

fold = 0
for train_idx, val_idx in tss.split(df):
    train = df.iloc[train_idx]
    test = df.iloc[val_idx]

    X_train, y_train = train[FEATURES], train[TARGET]
    X_test, y_test = test[FEATURES], test[TARGET]

    reg = xgb.XGBRegressor(
        base_score=0.5,
        booster="gbtree",
        n_estimators=500,
        early_stopping_rounds=50,
        objective="reg:linear",
        max_depth=3,
        learning_rate=0.01,
    )

    print(f"Training fold {fold}...")
    reg.fit(
        X_train, y_train, eval_set=[(X_train, y_train), (X_test, y_test)], verbose=100
    )
    fold += 1
