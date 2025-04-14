# Energy Consumption Forcasting Using Time-Series Data

Python version: 3.11.7 <br/>

This project focuses on predicting energy consumption for a specific region using historical time-series data. The dataset includes energy usage values measured in megawatts (MW), which are essential for identifying patterns and making informed decisions in energy management.

The primary objective is to develop a model that accurately forecasts future energy consumption based on historical trends. This notebook walks through the full pipeline, from data exploration and feature engineering to model training and evaluation, placing an emphasis on handling time-series data, which presents unique challenges due to its temporal dependencies.

### Dataset <br/>
The dataset is sourced from Kaggle and contains the following original columns:

- Datetime: Timestamp of the observation

- AEP_MW: Energy consumption (in megawatts)

### Engineered Features <br/>
To enhance model performance, several additional features were extracted from the Datetime column:

- hour: Hour of the day

- day_of_week: Day of the week (0 = Monday, 6 = Sunday)

- quarter: Year quarter (1–4)

- month: Month (1–12)

- year: Year of the observation

- day_of_year: Day of the year (1–365)

- day: Day of the month

### Holiday Indicators <br/>
Several holidays were also incorporated as binary features to capture potential consumption patterns:

- christmas

- halloween

- fourth_of_july

- thanksgiving

- easter

- new_year

For some holidays, like Halloween, Fourth of July, and New Years, an additional heuristic was applied to account for "party holidays". If the actual holiday doesn't fall on a weekend, it's assumed that celebrations may occur on the nearest weekend. Although this approach slightly worsened the RMSE compared to using only the actual holiday dates, it was an intentional design choice to test the hypothesis that celebration-adjusted days may impact energy usage.

🚧 TODO
Clean up EDA notebook and create .py files

