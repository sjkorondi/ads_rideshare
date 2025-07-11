import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class GUI():
    def __init__(self, root, expected, cars, total, indiv):
        self.root = root
        self.expected = expected
        self.cars = cars
        self.total = total
        self.indiv = indiv

        self.distance = 0
        self.petrol = 0

        # expected distance / weighted average of fuel economies * average fuel cost per litre in Germany
        self.forecasted_petrol = round(((self.expected / (18 * 0.7 + 14 * 0.3)) * 1.67), 2)
        self.forecasted_maintenance = 0
        
        self.forecasted_operational = 0

        for car in cars:
            self.petrol += round(car.getLitres() * 1.67, 2)
            self.distance += car.getDriven()

        self.petrol = round(self.petrol, 2)

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
                            "leads us to estimate operational costs of 2025 at €{}.".format(
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

            backButton = tk.Button(buttonFrame, text=">",command=self.transitionScreen)
            backButton.pack()

    def transitionScreen(self):
            self.clear()

            for car in self.cars:
                 car.resetMaintenance()

            tk.Label(self.root,
                    bg="white", 
                    font=("Arial", 16, "bold"),
                    padx=10, pady=10,
                    text="*2025 happens...*").pack(fill=tk.BOTH,expand=True)
            
            buttonFrame = tk.Frame(self.root, bg="white")
            buttonFrame.pack(fill=tk.BOTH,expand=True)

            backButton = tk.Button(buttonFrame, text="<",command=self.estimateScreen)
            backButton.pack()
