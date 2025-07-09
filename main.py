import matplotlib.pyplot as plt
import pandas as pd

df = pd.read_csv(r"data\cleaned_sorted_ride_data.csv")

df['date'] = pd.to_datetime(df['date'], format='mixed', errors='coerce')
df['distance'] = df['distance'] // 1
df["month"] = df["date"].dt.month

pivot = df.pivot_table(values="distance",index="vehicle",columns="month")

pivot.plot(kind="bar", stacked=False, colormap="Set2")
plt.title("Miles Driven By Vehicle Per Month")
plt.ylabel("Miles Driven")
plt.xlabel("Vehicle")
plt.grid(axis='y', linestyle='--', alpha=0.6)
plt.tight_layout()
plt.show()