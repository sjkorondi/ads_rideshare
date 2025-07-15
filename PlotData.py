from matplotlib.figure import Figure

def makeForecastPlot(full_df): # plot the provided dataframe (assumes dataframe given from PastTrips module)
    fig = Figure(figsize=(12,6), dpi=100)
    ax = fig.add_subplot(111)

    for label, group in full_df.groupby("type"): # graphs both the actual data and forecasted data
        ax.plot(group["date"], group["total_distance"], label=label, marker='o', linestyle='--' if label == "Forecast" else '-')

    for _, row in full_df.iterrows(): # text displaying the exact distance driven that month
        ax.text(row["date"], row["total_distance"] + 10,
                str(row["total_distance"]),
                fontsize=8,
                ha='center',
                va='bottom')

    ax.set_title("Total Distance Driven Per Month With Forecast")
    ax.set_xlabel("Date, YYYY-MM")
    ax.set_ylabel("Distance Driven, km")
    ax.grid(True, linestyle='--', alpha=0.6)
    ax.legend()

    return fig

def makeCarPlot(cars):
    fig = Figure(figsize=(12,6), dpi=100)
    ax = fig.add_subplot(111)

    for car in cars:
        ax.bar(car.getId(), car.getDriven()) # puts bars showing the car ID on the x axis and the distance that car drove on the y axis
        ax.text(car.getId(), car.getDriven() + 10, # shows text displaying the exact distance driven by a car
                str(car.getDriven()),
                fontsize=8,
                ha='center',
                va='bottom')

    ax.set_title("Total Distance Driven By Car") # styles the figure
    ax.set_xlabel("Vehicle ID")
    ax.set_ylabel("Distance Driven, km")
    ax.grid(True, linestyle='--', alpha=0.6)

    return fig