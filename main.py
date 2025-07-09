import matplotlib.pyplot as plt
import pandas as pd
from data import random_data_generator as rdg

rdg.run() # generates data for past trips

df = pd.read_csv(r"data\cleaned_sorted_ride_data.csv") # loads past trips

df['date'] = pd.to_datetime(df['date'], format='mixed', errors='coerce') # cleans data for graphing
df['distance'] = df['distance'] // 1
df["month"] = df["date"].dt.month
df["year"] = df["date"].dt.year

pivot = df.pivot_table(values="distance",index="year",columns="month", aggfunc="sum") # creates pivot table for the graph, displays sum
long_df = pivot.reset_index().melt(id_vars="year", var_name="month", value_name="total_distance")

# Create a datetime column for plotting
long_df["day"] = 1  # Set dummy day
long_df["date"] = pd.to_datetime(dict(year=long_df["year"], month=long_df["month"], day=long_df["day"]))

# Sort by actual date
long_df = long_df.sort_values("date")

# Plot the line graph
plt.figure(figsize=(10, 6))
plt.plot(long_df["date"], long_df["total_distance"], marker="o", linestyle="-")

plt.title("Total Distance Driven Per Month")
plt.xlabel("Date")
plt.ylabel("Distance Driven")
plt.grid(True, linestyle='--', alpha=0.6)
plt.tight_layout()
plt.show()