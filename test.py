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

future = df_and_future.query("is_future").copy()

reg = xgb.XGBRegressor()
reg.load_model("model.json")

# Predict future consumption
future["prediction"] = reg.predict(future[FEATURES])

# Save or plot results
future[["prediction"]].to_csv("future_predictions.csv")
