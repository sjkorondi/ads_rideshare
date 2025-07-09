import matplotlib.pyplot as plt
import pandas as pd

from data import RandomDataGenerator as rdg
import PlotData
import PastTrips
import Car

if __name__ == "__main__":
    car_list = [] # initialize a list of cars
    for i in range(10):
        car_list.append(Car.Car(True if i <= 6 else False)) # first seven are light, last three are heavy

    rdg.run() # generate data for past trips

    df = pd.read_csv(r"data\cleaned_sorted_ride_data.csv") # load past trips
    full_df = PastTrips.runPastTrips(df) # get forecasted data from past trips

    for row in df.itertuples(index=False): # assign each car the distance it drove in the past
        car_list[row.vehicle - 1].updateDriven(row.distance)

    PlotData.plot(full_df) # plot data