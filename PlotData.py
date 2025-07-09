import matplotlib.pyplot as plt

def plot(full_df):
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