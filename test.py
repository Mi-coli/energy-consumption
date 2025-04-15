import pandas as pd
import xgboost as xgb
from helper_functions import *


df = pd.read_csv("AEP_hourly.csv", parse_dates=["Datetime"], index_col="Datetime")
df = df.query("AEP_MW > 9700 and AEP_MW < 24700").copy()

df = feature_extraction(df)
df = create_lag(df)

# Forecast future dates
future_dates = pd.date_range("2018-08-03", "2019-08-03", freq="1h")
future_df = pd.DataFrame(index=future_dates)
future_df["is_future"] = True
df["is_future"] = False

df_and_future = pd.concat([df, future_df])
df_and_future = feature_extraction(df_and_future)
df_and_future = create_lag(df_and_future)

future = df_and_future.query("is_future")

reg = xgb.XGBRegressor(
    base_score=0.5,
    booster="gbtree",
    n_estimators=500,
    #early_stopping_rounds=50,
    objective="reg:linear",
    max_depth=3,
    learning_rate=0.01,
)

# For simplicity in this demo, train on entire df (in reality you'd load a trained model)
reg.fit(df[FEATURES], df[["AEP_MW"]])

# Predict future consumption
future = future.copy() # This isn't necessary, but I want to get rid of a warning that's a bit annoying
future["prediction"] = reg.predict(future[FEATURES])

# Save or plot results
future[["prediction"]].to_csv("future_predictions.csv")
