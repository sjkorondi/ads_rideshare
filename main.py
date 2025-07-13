import pandas as pd
import tkinter as tk

from data import RandomDataGenerator as rdg
import PlotData
import PastTrips
import Car
import GUI

PETROL_PRICE = 1.67 # average petrol price (euros/litre) in Germany as of 07/07/2025
petrol_spending = 0
distance_driven = 0

if __name__ == "__main__":
    car_list = [] # initialize a list of cars
    for i in range(10):
        car_list.append(Car.Car(i + 1, True if i <= 6 else False)) # first seven are light, last three are heavy

    rdg.generatePast() # generate data for past trips
    rdg.generateCurrent() # generate data for future trips

    past_df = pd.read_csv(r"data\cleaned_sorted_ride_data.csv") # load past trips
    full_df = PastTrips.runPastTrips(past_df) # get forecasted data from past trips
    forecasted_distance = 0

    future_df = pd.read_csv(r"data\cleaned_sorted_future_data.csv") # load future data

    for row in full_df.itertuples(): # calculate the total forecasted distance
        forecasted_distance += row.total_distance if row.type == "Forecast" else 0

    for row in past_df.itertuples(index=False): # assign each car the distance it drove in the past
        car_list[row.vehicle - 1].updateDriven(row.distance)

    root = tk.Tk()
    root.title("Fahrgemeinschaft Deutschland - 2025 Forecasting and Scheduling")
    forecast_plot = PlotData.makeForecastPlot(full_df)
    car_plot = PlotData.makeCarPlot(car_list)

    gui = GUI.GUI(root, forecasted_distance, car_list, forecast_plot, car_plot, future_df)

    root.mainloop()