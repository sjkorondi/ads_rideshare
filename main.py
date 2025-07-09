import matplotlib.pyplot as plt
import pandas as pd

from data import RandomDataGenerator as rdg
import PlotData
import PastTrips
import Car

PETROL_PRICE = 1.67 # average petrol price (euros/litre) in Germany as of 07/07/2025
petrol_spending = 0
distance_driven = 0

if __name__ == "__main__":
    car_list = [] # initialize a list of cars
    for i in range(10):
        car_list.append(Car.Car(True if i <= 6 else False)) # first seven are light, last three are heavy

    rdg.generate() # generate data for past trips

    df = pd.read_csv(r"data\cleaned_sorted_ride_data.csv") # load past trips
    full_df = PastTrips.runPastTrips(df) # get forecasted data from past trips

    for row in df.itertuples(index=False): # assign each car the distance it drove in the past
        car_list[row.vehicle - 1].updateDriven(row.distance)

    for car in car_list:
        petrol_spending += round(car.getLitres() * PETROL_PRICE, 2)
        distance_driven += car.getDriven()

    print("Total euros spent on petrol: " + str(round(petrol_spending, 2))) # rounding here because floating point issues
    print("Total kilometers driven: " + str(distance_driven))

    PlotData.plot(full_df) # plot data

    def extractCarID ():
        return [
        {"id": 1},
        {"id": 2},
        {"id": 3},
        {"id": 4},
        {"id": 5},
        {"id": 6},
        {"id": 7},
        {"id": 8},
        {"id": 9},
        {"id": 10},

        ]
    
def classify_car(car_id):
    if 1<= car_id <= 7:
        print ('The car is light.')

    elif 8<= car_id <=10:
        print ('The car is heavy.')
    else:
        print ('Invalid car ID.')

def pick_car (passenger_count, vehicles):
    light_vehicle = [v for v in vehicles if classify_car (v["id"]) == "light"]
    heavy_vehicle = [v for v in vehicles if classify_car (v["id"]) == "heavy"]
    
    if passenger_count > 3:
        return "heavy"
    
    if passenger_count <= 3:
        all_light_vehicles_need_maintenance = all (v["need maintenance"] for v in light_vehicle)
        all_heavy_vehicles_need_maintenance = all (v["need maintenance"] for v in heavy_vehicle)

    if all_light_vehicles_need_maintenance:
        if all_heavy_vehicles_need_maintenance:
            return "light"
        else:
            return "heavy"
    else: 
        return "light"