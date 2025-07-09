import pandas as pd

def runPastTrips(df):
    df["date"] = pd.to_datetime(df["date"], format="mixed", errors="coerce") # clean data for graphing
    df["month"] = df["date"].dt.month
    df["year"] = df["date"].dt.year

    pivot = df.pivot_table(values="distance",index="year",columns="month", aggfunc="sum") # creates pivot table for the graph, displays sum
    long_df = pivot.reset_index().melt(id_vars="year", var_name="month", value_name="total_distance")

    # create datetime column for plotting
    long_df["day"] = 1  # dummy day
    long_df["date"] = pd.to_datetime(dict(year=long_df["year"], month=long_df["month"], day=long_df["day"]))

    long_df = long_df.sort_values("date") # sort by actual date

    latest_year = long_df["year"].max() # get year for forecasting
    forecast_year = latest_year + 1

    monthly_avg = ( # calculate average distance driven per month for past three years
        long_df[long_df["year"] >= latest_year - 2]
        .groupby("month")["total_distance"]
        .mean()
        .round()
        .astype(int)
    )

    forecast_df = pd.DataFrame({ # build forecast dataframe
        "year": forecast_year,
        "month": monthly_avg.index,
        "total_distance": monthly_avg.values,
    })
    forecast_df["day"] = 1
    forecast_df["date"] = pd.to_datetime(dict(year=forecast_df["year"], month=forecast_df["month"], day=forecast_df["day"]))
    forecast_df["type"] = "Forecast"
    long_df["type"] = "Actual"

    full_df = pd.concat([long_df, forecast_df], ignore_index=True) # combine data

    return full_df
