class Bin:
    def __init__(self, name,lat, long, full, weight):
        self.name = name #this is the name is the variable - useful for printing out the information about the bin but can delete this later
        self.lat = lat #float for latitude of bin
        self.long = long #float for longitude of bin
        self.full = full #boolean for whether bin is full - True means it's full
        self.weight = weight #float for weight of the bin
    def get_location(self): #returns location
        return self.lat, self.long
    def get_weight(self): 
        return self.weight
    def update(self, latitude, longitude, fullState, weight):
        self.lat = latitude
        self.long = longitude
        self.full = fullState
        self.weight = weight
    def __str__(self):
        if self.full == True:
            return f"{self.name} has latitude {self.lat:.2f}, longitude {self.long:.2f}, is full, and has weight {self.weight:.2f} kg" 
        #note can't do print self which is why I used self.name
        else:
            return f"{self.name} has latitude {self.lat:.2f}, longitude {self.long:.2f} , is not full, and has weight {self.weight:.2f} kg " 


   



