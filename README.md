# Energy Consumption Prediction Using Time-Series Data

In this project, I aim to predict the energy consumption for a specific region using historical time-series data. The dataset contains energy usage values measured in megawatts, which are crucial for understanding patterns and making informed decisions in energy management.

The objective of this analysis is to develop a model capable of forecasting future energy consumption based on past trends. This notebook demonstrates the process of time-series forecasting, from data exploration and feature engineering to model development and evaluation. Time-series data requires specific handling due to its temporal structure, making this task both challenging and valuable for accurate predictions.

Input Features:
- The input data comes from a Kaggle dataset, and consists of two columns: <br/>
      - "Datetime" <br/>
      - "AEP_MW": Megawatts per hour <br/>
- I also extracted a few more features, including Holidays, from the "Datetime" in order to increase the model accuracy:
      - "hour": hour in the day
      - "day_of_week": day of week, numbered 0 - 6
      - "quarter": dividing the year into 4 quarters
      - "month": month of the year
      - "year"
      - "day_of_the_year": days numbered from 1 - 365
      - "day": day of the month, 1 - 28/29/30/31
      - "christmas"
      - "halloween"
      - "fouth_of_july"
      - "thanksgiving"
      - "easter"

In addition to extracting the Holidays, I also wanted to consider that a few of them are considered "party holidays", meaning that if the actual Holiday doesn't fall on the weekend, then we can assume that it is also getting celebrated on the nearest weekend to the actual day (such as Halloween, 4th of July, and New Year). This is an overkill and does result in a slightly worse RMSE than the model which only considered the actual holiday days, however I do think this was something worth considering initially, so I will leave it in.   
