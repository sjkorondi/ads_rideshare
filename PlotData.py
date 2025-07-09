import matplotlib.pyplot as plt

def plot(full_df): # plot the provided dataframe (assumes dataframe given from PastTrips module)
    plt.figure(figsize=(12, 6))
    ax = plt.gca()

    for label, group in full_df.groupby("type"):
        ax.plot(group["date"], group["total_distance"], label=label, marker='o', linestyle='--' if label == "Forecast" else '-')

    for _, row in full_df.iterrows():
        ax.text(row["date"], row["total_distance"] + 10,
                str(row["total_distance"]),
                fontsize=8,
                ha='center',
                va='bottom')

    plt.title("Total Distance Driven Per Month with Forecast")
    plt.xlabel("Date")
    plt.ylabel("Distance Driven")
    plt.grid(True, linestyle='--', alpha=0.6)
    plt.legend()
    plt.tight_layout()
    plt.show()