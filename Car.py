class Car():
    def __init__(self, type: bool):
        self.type = type
        self.miles_driven = 0
        self.maintenance_miles = 3000 if type else 2000 # true for light, false for heavy
    
    def getType(self):
        return self.type

    def getMaintenanceMiles(self):
        return self.maintenance_miles

    def updateDriven(self, miles: int):
        self.miles_driven += miles

    def getDriven(self):
        return self.miles_driven

    def checkMaintenance(self): # if the care has driven enough, it requires maintenance
        return self.miles_driven >= self.maintenance_miles