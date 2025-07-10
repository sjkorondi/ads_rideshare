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
        for car in cars:
            self.petrol += round(car.getLitres() * 1.67, 2)
            self.distance += car.getDriven()
        
        self.petrol = round(self.petrol, 2)

        self.homeScreen()

    def clear(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def homeScreen(self):
        self.clear()
        tk.Label(self.root,
                 bg="white", 
                 font=("Arial", 16, "bold"),
                 padx=10, pady=10,
                 text="Welcome to our projections for the costs of\n" \
                        "running our ridesharing business in 2025.").pack(fill=tk.BOTH,expand=True)
        
        forwardButton = tk.Button(self.root, text=">",command=self.totalMilesDriven)
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
                text="If our forecasted (mean) total distance of {} kilometers is achieved, it is expected to cost us €{} in petrol.".format(
                    self.expected,  
                    round(((self.expected / (18 * 0.7 + 14 * 0.3)) * 1.67), 2)) # forecasted distance / weighted average of fuel economies * average petrol price
                ).pack(fill=tk.BOTH,expand=True)
        
        forwardButton = tk.Button(self.root, text=">",command=self.indivCars)
        forwardButton.pack()

        backButton = tk.Button(self.root, text="<",command=self.homeScreen)
        backButton.pack()
        
    def indivCars(self):
        self.clear()
        car_canvas = FigureCanvasTkAgg(self.indiv, master=self.root)
        car_canvas.draw()
        car_canvas.get_tk_widget().pack(fill=tk.BOTH,expand=True)

        avg_distance = round(self.distance / 30) # total distance across three years across ten cars

        maintenance_needed = ""
        maintenance_int = 0

        for car in self.cars: # if a car needed maintenance
            if car.checkMaintenance():
                maintenance_needed += (str(car.getId()) + ", ")
                maintenance_int += 1

        maintenance_needed = maintenance_needed.removesuffix(", ")

        tk.Label(self.root, 
                bg="white", 
                font=("Arial", 16, "bold"), 
                text="These are the distances driven by each individual vehicle over the past three years." \
                    "\n Each vehicle drove an average of {} kilometers per year.".format(avg_distance)
                ).pack(fill=tk.BOTH,expand=True)
        
        tk.Label(self.root, 
                bg="white", 
                font=("Arial", 16, "bold"), 
                text="Vehicles {} required maintenance during this time.".format(maintenance_needed) if maintenance_int > 0 else "No vehicles required maintenance during this time."
                ).pack(fill=tk.BOTH,expand=True)
        
        backButton = tk.Button(self.root, text="<",command=self.totalMilesDriven)
        backButton.pack()
