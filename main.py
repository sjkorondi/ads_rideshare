import matplotlib.pyplot as plt
import pandas as pd

df = pd.read_csv(r"data\cleaned_sorted_ride_data.csv")

df['date'] = pd.to_datetime(df['date'], format='mixed', errors='coerce')
df['distance'] = df['distance'] // 1
df["month"] = df["date"].dt.month
df["year"] = df["date"].dt.year

pivot = df.pivot_table(values="distance",index="year",columns="month")

last_date = df['date'].max()

pivot.plot(kind="bar", stacked=False, colormap="Set2")
plt.title("Miles Driven Per Month Per Year")
plt.ylabel("Miles Driven")
plt.xlabel("Year/Month")
plt.grid(axis='y', linestyle='--', alpha=0.6)
plt.tight_layout()
plt.show()