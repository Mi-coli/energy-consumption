import pandas as pd
from dateutil.easter import easter

# Define train and target features to use for the model
FEATURES = [
    "hour",
    "day_of_week",
    "month",
    "year",
    "day_of_year",
    "day",
    "christmas",
    "thanksgiving",
    "lag_one_year",
    "lag_two_years",
    "lag_three_years",
]
TARGET = ["AEP_MW"]


def feature_extraction(df):
    """
    Extracts time-based and holiday-related features from a DataFrame with a datetime index.
    Will also find nearest Friday and Saturday to Halloween, 4th of July, and New Years, since this is
    when these holidays are most likely to be celebrated if the holiday itself doesn't fall
    on a Friday or Saturday

    Parameters:
        df (pd.DataFrame): A DataFrame with a DatetimeIndex.

    Returns:
        pd.DataFrame: The input DataFrame with new datetime and holiday features.
    """
    df = df.copy()
    df["hour"] = df.index.hour
    df["day_of_week"] = df.index.dayofweek
    df["quarter"] = df.index.quarter
    df["month"] = df.index.month
    df["year"] = df.index.year
    df["day_of_year"] = df.index.dayofyear
    df["day"] = df.index.day

    df["new_year"] = ((df["day"] == 1) & (df["month"] == 1)).astype(int)
    df["christmas"] = ((df["month"] == 12) & (df["day"] == 25)).astype(int)
    df["halloween"] = ((df["month"] == 10) & (df["day"] == 31)).astype(int)
    df["fourth_of_july"] = ((df["month"] == 7) & (df["day"] == 4)).astype(int)

    for holiday, col_name in [
        ("Halloween", "halloween"),
        ("4th of July", "fourth_of_july"),
        ("New Year", "new_year"),
    ]:
        holiday_dates = df[df[col_name] == 1].index
        for date in holiday_dates:
            if date.weekday() not in [
                4,
                5,
            ]:  # Check if the holidays fall on Friday (4) or Saturday(5)
                nearest_friday = date + pd.DateOffset(days=(4 - date.weekday()) % 7)
                nearest_saturday = nearest_friday + pd.DateOffset(days=1)

                if nearest_friday in df.index:
                    df.loc[nearest_friday, col_name] = 1
                if nearest_saturday in df.index:
                    df.loc[nearest_saturday, col_name] = 1

    df["thanksgiving"] = (
        (df["month"] == 11)
        & (df["day_of_week"] == 3)
        & (df["day"] >= 22)
        & (df["day"] <= 28)
    ).astype(int)

    df["easter_date"] = df["year"].apply(lambda year: easter(year))
    df["easter"] = (df.index.date == df["easter_date"]).astype(int)
    df.drop(columns=["easter_date"], inplace=True)

    return df


def create_lag(df, target_col="AEP_MW"):
    """
    Adds lag features based on the previous one, two, and three years (364-day intervals).

    Parameters:
        df (pd.DataFrame): A DataFrame with a datetime index and target column.
        target_col (str): Column name for the target variable.

    Returns:
        pd.DataFrame: DataFrame with lag features.
    """
    target_map = df[target_col].to_dict()
    df["lag_one_year"] = (df.index - pd.Timedelta("364 days")).map(target_map)
    df["lag_two_years"] = (df.index - pd.Timedelta("728 days")).map(target_map)
    df["lag_three_years"] = (df.index - pd.Timedelta("1092 days")).map(target_map)
    return df
