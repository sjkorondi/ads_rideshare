class Car():
    def __init__(self, id: int, type: bool): # true for light, false for heavy
        self.id = id
        self.type = type
        self.kilos_driven = 0
        self.litres_burnt = 0
        self.maintenance_kilos = 2600 if type else 2000 # light vehicles require less maintenance
        self.kilos_per_litre = 18 if type else 14 # light vehicles get better fuel economy
        self.maintenance_needed = False

    def getId(self):
        return self.id

    def getType(self):
        return self.type

    def getDriven(self):
        return self.kilos_driven
    
    def updateDriven(self, kilos: int):
        self.kilos_driven += kilos
        self.litres_burnt += (kilos / self.kilos_per_litre)

    def getLitres(self):
        return self.litres_burnt

    def getMaintenanceKilos(self):
        return self.maintenance_kilos

    def checkMaintenance(self): # if the car has driven enough, it requires maintenance
        self.maintenance_needed = self.kilos_driven >= self.maintenance_kilos
        return self.maintenance_needed
    
    def resetMaintenance(self):
        if self.checkMaintenance:
            self.kilos_driven -= self.maintenance_kilos
    
    def hypoMaintenance(self, extra: int):
        return ((self.kilos_driven + extra) >= self.maintenance_kilos) and (not self.maintenance_needed)