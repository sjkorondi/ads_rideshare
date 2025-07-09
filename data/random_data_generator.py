import csv
import random
import pandas as pd

NUM_DATES = 200
MONTHS = list(range(1,13))
MONTH_WEIGHTS = [ # bias weights, simulating more business during summer months
    1,2,2,3,
    3,4,4,3,
    3,2,2,1
]

def pickRandomDay(month: int): # generate a random day of the month
    if month == 2: # February has 28 days (ignoring leap years)
        return random.randint(1,28)
    elif month in [1,3,5,7,8,10,12]: # checking for months with 31 days
        return random.randint(1,31)
    else: # otherwise it has 30 days
        return random.randint(1,30)

def pickBiasedMonth():
    return random.choices(MONTHS, weights=MONTH_WEIGHTS, k=1)[0]

def pickYear(num_gen: int):
    if num_gen < NUM_DATES / 2:
        return 2023
    else:
        return 2024
    
def generateDate(num_gen: int):
    year = pickYear(num_gen=num_gen)
    month = pickBiasedMonth()
    day = pickRandomDay(month=month)

    formatted_date = f"{year:04d}-{month:02d}-{day:02d}" # yyyy-mm-dd with trailing zeroes

    return formatted_date

def createRandomData():
    with open(r"data\random_ride_data.csv", 'w', newline='') as csvfile: # writes randomly generated data to a .csv file (already made, not needed)
        fieldnames = ['vehicle', 'date', 'distance']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        for x in range(NUM_DATES):
            writer.writerow({
                'vehicle': random.randint(1,10), # business owns 10 vehicles
                'date': generateDate(x),
                'distance': random.randint(10,50) # vehicle drives anywhere from 10 to 50 kilometers in one trip
            })

def run():
    createRandomData()
    df = pd.read_csv(r"data\random_ride_data.csv")

    df['vehicle'] = df['vehicle'].astype(int) # cleaning data
    df['date'] = pd.to_datetime(df['date'], format='mixed', errors='coerce')
    df['distance'] = df['distance'].astype(int)

    df = df.sort_values('date').reset_index(drop=True) # sorting data by the date

    df.to_csv(r"data\cleaned_sorted_ride_data.csv", index=False) # save cleaned and sorted data