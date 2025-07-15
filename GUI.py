import tkinter as tk
import pandas as pd
import random
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

import PlotData


class GUI():
        def __init__(self, root, expected, cars, total, indiv, future):
                self.root = root
                self.expected = expected # forecasted distance to be driven
                self.cars = cars # list of cars available to the company
                self.total = total
                self.indiv = indiv
                self.future = future

                self.distance = 0
                self.petrol = 0

                for car in cars:
                        self.petrol += round(car.getLitres() * 1.67, 2)
                        self.distance += car.getDriven()

                self.petrol = round(self.petrol, 2)

                # expected distance / weighted average of fuel economies * average fuel cost per litre in Germany
                self.forecasted_petrol = round(((self.expected / (18 * 0.7 + 14 * 0.3)) * 1.67), 2)
                self.forecasted_maintenance = 0
                self.forecasted_cost = 0

                self.future_distance = 0
                self.future_maintenance = 0
                self.future_maintenance_list = []
                self.future_petrol = 0
                self.future_operational = 0

                self.homeScreen()

        def clear(self):
                for widget in self.root.winfo_children(): # clear all widgets in a window
                        widget.destroy()

        def homeScreen(self):
                self.clear()
                tk.Label(self.root,
                        bg="white", 
                        font=("Arial", 16, "bold"),
                        padx=10, pady=10,
                        text="Welcome to our projections for the costs of\n" \
                        "running our ridesharing business in 2025.").pack(fill=tk.BOTH,expand=True)

                buttonFrame = tk.Frame(self.root, bg="white")
                buttonFrame.pack(fill=tk.BOTH,expand=True)

                forwardButton = tk.Button(buttonFrame, text=">",command=self.totalMilesDriven)
                forwardButton.pack()

        def totalMilesDriven(self):
                self.clear()
                forecast_canvas = FigureCanvasTkAgg(self.total, master=self.root)
                forecast_canvas.draw()
                forecast_canvas.get_tk_widget().pack(fill=tk.BOTH,expand=True)

                tk.Label(self.root, 
                bg="white", 
                font=("Arial", 16, "bold"), 
                text="Over the past three years, company vehicles drove {} kilometers, costing us €{} in petrol.".format(
                        self.distance, 
                        self.petrol)
                ).pack(fill=tk.BOTH,expand=True)

                tk.Label(self.root, 
                bg="white", 
                font=("Arial", 16, "bold"), 
                text="Our forecasted (mean) total distance of {} kilometers is expected to cost us €{} in petrol.".format(
                        self.expected,  
                        self.forecasted_petrol) # forecasted distance / weighted average of fuel economies * average petrol price
                ).pack(fill=tk.BOTH,expand=True)

                buttonFrame = tk.Frame(self.root, bg="white")
                buttonFrame.pack(fill=tk.BOTH, expand=True)

                backButton = tk.Button(buttonFrame, text="<",command=self.homeScreen)
                backButton.pack()

                forwardButton = tk.Button(buttonFrame, text=">",command=self.indivCars)
                forwardButton.pack()

        def indivCars(self):
                self.clear()
                car_canvas = FigureCanvasTkAgg(self.indiv, master=self.root)
                car_canvas.draw()
                car_canvas.get_tk_widget().pack(fill=tk.BOTH,expand=True)

                maintenance_needed = ""
                maintenance_count = 0

                for car in self.cars: # if a car needed maintenance
                        if car.checkMaintenance():
                                maintenance_needed += (str(car.getId()) + ", ")
                                maintenance_count += 1

                maintenance_needed = maintenance_needed.removesuffix(", ")

                tk.Label(self.root, 
                bg="white", 
                font=("Arial", 16, "bold"), 
                text="These are the distances driven by each individual vehicle over the past three years."
                ).pack(fill=tk.BOTH,expand=True)

                tk.Label(self.root, 
                bg="white", 
                font=("Arial", 16, "bold"), 
                text="Vehicles {} required maintenance during this time.".format(maintenance_needed) if maintenance_count > 0 else "No vehicles required maintenance during this time."
                ).pack(fill=tk.BOTH,expand=True)

                forecasted_average_distance = round(self.expected / 10)

                tk.Label(self.root, 
                bg="white", 
                font=("Arial", 16, "bold"), 
                text="Based on the forecasted distance, each vehicle is expected to drive {} kilometers this year.".format(forecasted_average_distance)
                ).pack(fill=tk.BOTH,expand=True)

                maintenance_needed = ""
                maintenance_count = 0

                for car in self.cars: # if a car needed maintenance
                        if car.hypoMaintenance(forecasted_average_distance):
                                maintenance_needed += (str(car.getId()) + ", ")
                                maintenance_count += 1

                maintenance_needed = maintenance_needed.removesuffix(", ")
                self.forecasted_maintenance = maintenance_count * 300

                tk.Label(self.root, 
                bg="white", 
                font=("Arial", 16, "bold"), 
                text="This will require vehicles {} to receive maintenance. We expect this will cost us €{} in repairs.".format(maintenance_needed, self.forecasted_maintenance)
                ).pack(fill=tk.BOTH,expand=True)

                buttonFrame = tk.Frame(self.root, bg="white")
                buttonFrame.pack(fill=tk.BOTH, expand=True)

                backButton = tk.Button(buttonFrame, text="<",command=self.totalMilesDriven)
                backButton.pack()

                forwardButton = tk.Button(buttonFrame, text=">",command=self.estimateScreen)
                forwardButton.pack()

        def estimateScreen(self):
                self.clear()
                tk.Label(self.root,
                        bg="white", 
                        font=("Arial", 16, "bold"),
                        padx=10, pady=10,
                        text="The forecasted petrol costs of €{} plus the forecasted maintenance costs of €{}\n" \
                                "leads us to estimate the operational costs of 2025 at €{}.".format(
                                self.forecasted_petrol, 
                                self.forecasted_maintenance, 
                                self.forecasted_maintenance + self.forecasted_petrol)
                                ).pack(fill=tk.BOTH,expand=True)

                self.forecasted_operational = round((self.forecasted_maintenance + self.forecasted_petrol) / self.expected, 2)

                tk.Label(self.root,
                        bg="white", 
                        font=("Arial", 16, "bold"),
                        padx=10, pady=10,
                        text="To cover the operational costs, with our estimated total distance of {} kilometers, \n" \
                        "it is recommended to charge at least €{} per kilometer driven.".format(
                                self.expected, 
                                self.forecasted_operational
                                )).pack(fill=tk.BOTH,expand=True)

                buttonFrame = tk.Frame(self.root, bg="white")
                buttonFrame.pack(fill=tk.BOTH,expand=True)

                backButton = tk.Button(buttonFrame, text="<",command=self.indivCars)
                backButton.pack()

                forwardButton = tk.Button(buttonFrame, text=">",command=self.transitionScreen)
                forwardButton.pack()

        def transitionScreen(self):
                self.clear()
                for car in self.cars:
                        car.resetMaintenance()

                tk.Label(self.root,
                bg="white", 
                font=("Arial", 16, "bold"),
                padx=10, pady=10,
                text="*2025 happens...*").pack(fill=tk.BOTH,expand=True)

                tk.Label(self.root,
                bg="white", 
                font=("Arial", 16, "bold"),
                padx=10, pady=10,
                text="Any vehicle that required maintenance has had its distance reset, \nto reflect it no longer needing maintenance.").pack(fill=tk.BOTH,expand=True)

                buttonFrame = tk.Frame(self.root, bg="white")
                buttonFrame.pack(fill=tk.BOTH,expand=True)

                backButton = tk.Button(buttonFrame, text="<",command=self.estimateScreen)
                backButton.pack()

                forwardButton = tk.Button(buttonFrame, text=">",command=self.futureScreen)
                forwardButton.pack()

        def future_calculations(self):
                light_cars = [car for car in self.cars if car.getType()]
                heavy_cars = [car for car in self.cars if not car.getType()]

                for index, row in self.future.iterrows():
                        carType = False
                        self.future_distance += row.distance
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
                                self.future.at[index, 'vehicle'] = random.randint(1,7)
                                self.cars[row.vehicle - 1].resetMaintenance()
                                self.cars[row.vehicle - 1].updateDriven(row.distance)
                                all_lights_need_maintenance = False
                        elif(carType):
                                lowestIndex = 0
                                driven = light_cars[0].getDriven()
                                for i in range(7):
                                       if light_cars[i].getDriven() < driven:
                                              driven = light_cars[i].getDriven()
                                              lowestIndex = i

                                car = light_cars[lowestIndex]
                                self.future.at[index, 'vehicle'] = car.getId()
                                car.updateDriven(row.distance)
                                self.future_petrol += car.getLitresOneTrip(row.distance)

                                if car.resetMaintenance():
                                       self.future_maintenance += 1
                                       self.future_maintenance_list.append(lowestIndex)

                        elif(all_heavies_need_maintenance):
                                self.future.at[index, 'vehicle'] = random.randint(8,10)
                                self.cars[row.vehicle - 1].resetMaintenance()
                                self.cars[row.vehicle - 1].updateDriven(row.distance)
                                all_heavies_need_maintenance = False
                        else:
                                lowestIndex = 0
                                driven = heavy_cars[0].getDriven()
                                for i in range(3):
                                       if heavy_cars[i].getDriven() < driven:
                                              driven = heavy_cars[i].getDriven()
                                              lowestIndex = i

                                car = heavy_cars[lowestIndex]
                                self.future.at[index, 'vehicle'] = car.getId()
                                car.updateDriven(row.distance)
                                self.future_petrol += car.getLitresOneTrip(row.distance)

                                if car.resetMaintenance():
                                       self.future_maintenance += 1
                                       self.future_maintenance_list.append(lowestIndex)
               
        def futureScreen(self):
                self.clear()
                self.future_calculations()
                
                car_canvas = FigureCanvasTkAgg(PlotData.makeCarPlot(self.cars), master=self.root)
                car_canvas.draw()
                car_canvas.get_tk_widget().pack(fill=tk.BOTH,expand=True)

                maintenance_needed = ""
                maintenance_count = 0

                for item in self.future_maintenance_list:
                       maintenance_needed += (str(item) + ", ")
                       maintenance_count += 1

                maintenance_needed = maintenance_needed.removesuffix(", ")
                maintenance_cost = 0

                for car in self.cars:
                       if car.checkMaintenance():
                              maintenance_cost += 300

                self.future_operational = round(self.future_petrol * 1.67 + maintenance_cost, 2)

                tk.Label(self.root,
                bg="white", 
                font=("Arial", 16, "bold"),
                padx=10, pady=10,
                text="These are the distances driven by each car after 2025. Note this \nincludes distances from previous years, if no maintenance was required then.").pack(fill=tk.BOTH,expand=True)

                tk.Label(self.root, 
                bg="white", 
                font=("Arial", 16, "bold"), 
                text="Following our rules-based logic, " + ("vehicles {} required maintenance during this time.".format(maintenance_needed) if self.future_maintenance > 0 else "no vehicles required maintenance during this time.")
                ).pack(fill=tk.BOTH,expand=True)

                tk.Label(self.root, 
                bg="white", 
                font=("Arial", 16, "bold"), 
                text="This cost us €{} in maintenance costs.".format(maintenance_cost)
                ).pack(fill=tk.BOTH,expand=True)

                tk.Label(self.root, 
                bg="white", 
                font=("Arial", 16, "bold"), 
                text="The total distance driven in 2025 was {} kilometers, costing us €{} in petrol.".format(self.future_distance, self.future_petrol * 1.67)
                ).pack(fill=tk.BOTH,expand=True)

                tk.Label(self.root, 
                bg="white", 
                font=("Arial", 16, "bold"), 
                text="Thus, our total cost for 2025 was €{}.".format(self.future_petrol * 1.67 + maintenance_cost)
                ).pack(fill=tk.BOTH,expand=True)

                buttonFrame = tk.Frame(self.root, bg="white")
                buttonFrame.pack(fill=tk.BOTH,expand=True)

                backButton = tk.Button(buttonFrame, text="<",command=self.transitionScreen)
                backButton.pack()

                forwardButton = tk.Button(buttonFrame, text=">",command=self.compareScreen)
                forwardButton.pack()

        def compareScreen(self):
               self.clear()

               tk.Label(self.root, 
                bg="white", 
                font=("Arial", 16, "bold"), 
                text="The total distance driven in 2025 was {} kilometers. Compared to the forecasted {} kilometers, this leaves a difference of {} kilometers.".format(
                       self.future_distance, self.expected, self.future_distance - self.expected)
                ).pack(fill=tk.BOTH,expand=True)
               
               tk.Label(self.root, 
                bg="white", 
                font=("Arial", 16, "bold"), 
                text="Charging €{} per kilometer driven has given us €{} to cover operational costs.".format(
                       self.forecasted_operational, self.forecasted_operational * self.future_distance)
                ).pack(fill=tk.BOTH,expand=True)
               
               tk.Label(self.root, 
                bg="white", 
                font=("Arial", 16, "bold"), 
                text="With our operational costs being €{}, we have a difference of €{}.".format(
                       self.future_operational, self.future_operational - self.forecasted_operational * self.future_distance)
                ).pack(fill=tk.BOTH,expand=True)
               
               buttonFrame = tk.Frame(self.root, bg="white")
               buttonFrame.pack(fill=tk.BOTH,expand=True)
               
               backButton = tk.Button(buttonFrame, text="<",command=self.futureScreen)
               backButton.pack()
               
               forwardButton = tk.Button(buttonFrame, text=">",command=self.endScreen)
               forwardButton.pack()

        def endScreen(self):
               self.clear()

               tk.Label(self.root, 
                bg="white", 
                font=("Arial", 64, "bold"), 
                text="The End!"
                ).pack(fill=tk.BOTH,expand=True)
               
               buttonFrame = tk.Frame(self.root, bg="white")
               buttonFrame.pack(fill=tk.BOTH,expand=True)
               
               backButton = tk.Button(buttonFrame, text="<",command=self.compareScreen)
               backButton.pack()
               
               forwardButton = tk.Button(buttonFrame, text="Close",command=self.root.destroy)
               forwardButton.pack()


'''def classify_car(car_id):
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
'''