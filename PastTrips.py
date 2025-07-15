import pandas as pd
import random

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

def runFutureCalculations(df, cars):
                light_cars = [car for car in cars if car.getType()]
                heavy_cars = [car for car in cars if not car.getType()]

                for index, row in df.iterrows():
                        carType = False
                        all_lights_need_maintenance = all(car.hypoMaintenance(row.distance) for car in light_cars)
                        all_heavies_need_maintenance = all(car.hypoMaintenance(row.distance) for car in heavy_cars)

                        if(row.passengers > 3):
                                carType = False
                        else:
                                if(all_lights_need_maintenance):
                                        if(all_heavies_need_maintenance):
                                                carType = True
                                        else:
                                                carType = False
                                else:
                                        carType = True

                        if(carType and all_lights_need_maintenance):
                                df.at[index, 'vehicle'] = random.randint(1,7)
                                cars[row.vehicle - 1].resetMaintenance()
                                cars[row.vehicle - 1].updateDriven(row.distance)
                                all_lights_need_maintenance = False
                        elif(carType):
                                for car in light_cars:
                                        if car.hypoMaintenance(row.distance):
                                                pass
                                        else:
                                                df.at[index, 'vehicle'] = car.getId()
                                                car.updateDriven(row.distance)
                                                break
                        elif(not carType and all_heavies_need_maintenance):
                                df.at[index, 'vehicle'] = random.randint(8,10)
                                cars[row.vehicle - 1].resetMaintenance()
                                cars[row.vehicle - 1].updateDriven(row.distance)
                                all_heavies_need_maintenance = False
                        else:
                                for car in heavy_cars:
                                        if car.hypoMaintenance(row.distance):
                                                pass
                                        else:
                                                df.at[index, 'vehicle'] = car.getId()
                                                car.updateDriven(row.distance)
                                                break
               