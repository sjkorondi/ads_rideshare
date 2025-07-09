import matplotlib.pyplot as plt
import pandas as pd
from data import random_data_generator as rdg

MAINTENANCE_MILES = 3000

rdg.run() # generate data for past trips

df = pd.read_csv(r"data\cleaned_sorted_ride_data.csv") # load past trips

df["date"] = pd.to_datetime(df["date"], format="mixed", errors="coerce") # clean data for graphing
df["month"] = df["date"].dt.month
df["year"] = df["date"].dt.year

pivot = df.pivot_table(values="distance",index="year",columns="month", aggfunc="sum") # creates pivot table for the graph, displays sum
long_df = pivot.reset_index().melt(id_vars="year", var_name="month", value_name="total_distance")

# create datetime column for plotting
long_df["day"] = 1  # dummy day
long_df["date"] = pd.to_datetime(dict(year=long_df["year"], month=long_df["month"], day=long_df["day"]))

# sort by actual date
long_df = long_df.sort_values("date")

# get year for forecasting
latest_year = long_df["year"].max()
forecast_year = latest_year + 1

# calculate average distance driven per month for past three years
monthly_avg = (
    long_df[long_df["year"] >= latest_year - 2]
    .groupby("month")["total_distance"]
    .mean()
    .round()
    .astype(int)
)

# build forecast dataframe
forecast_df = pd.DataFrame({
    "year": forecast_year,
    "month": monthly_avg.index,
    "total_distance": monthly_avg.values,
})
forecast_df["day"] = 1
forecast_df["date"] = pd.to_datetime(dict(year=forecast_df["year"], month=forecast_df["month"], day=forecast_df["day"]))
forecast_df["type"] = "Forecast"
long_df["type"] = "Actual"

# combine data
full_df = pd.concat([long_df, forecast_df], ignore_index=True)

# plot data
plt.figure(figsize=(12, 6))
for label, group in full_df.groupby("type"):
    plt.plot(group["date"], group["total_distance"], label=label, marker='o', linestyle='--' if label == "Forecast" else '-')

plt.title("Total Distance Driven Per Month with Forecast")
plt.xlabel("Date")
plt.ylabel("Distance Driven")
plt.grid(True, linestyle='--', alpha=0.6)
plt.legend()
plt.tight_layout()
plt.show()