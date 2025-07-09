import matplotlib.pyplot as plt
import pandas as pd
from data import random_data_generator as rdg

rdg.run() # generate data for past trips

df = pd.read_csv(r"data\cleaned_sorted_ride_data.csv") # loads past trips

df['date'] = pd.to_datetime(df['date'], format='mixed', errors='coerce') # cleans data for graphing
df['distance'] = df['distance'] // 1
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




def extractCarID ():
    return [
        {"id": 1},
        {"id": 2},
        {"id": 3},
        {"id": 4},
        {"id": 5},
        {"id": 6},
        {"id": 7},
        {"id": 8},
        {"id": 9},
        {"id": 10},

        ]
    
def classify_car(car_id):
    if 1<= car_id <= 7:
        print ('The car is light.')

    elif 8<= car_id <=10:
        print ('The car is heavy.')
    else:
        print ('Invalid car ID.')

def pick_car (passenger_count, vehicles):
    light_vehicle = [v for v in vehicles if classify_car (v["id"]) == "light"]
    heavy_vehicle = [v for v in vehicles if classify_car (v["id"]) == "heavy"]
    
    if passenger_count > 3:
        return "heavy"
    
    if passenger_count <= 3:
        all_light_vehicles_need_maintenance = all (v["need maintenance"] for v in light_vehicle)
        all_heavy_vehicles_need_maintenance = all (v["need maintenance"] for v in heavy_vehicle)

    if all_light_vehicles_need_maintenance:
        if all_heavy_vehicles_need_maintenance:
            return "light"
        else:
            return "heavy"
    else: 
        return "light"
    

plt.title("Total Distance Driven Per Month with Forecast")
plt.xlabel("Date")
plt.ylabel("Distance Driven")
plt.grid(True, linestyle='--', alpha=0.6)
plt.legend()
plt.tight_layout()
plt.show()