class Bin:
    def __init__(self, lat, long, full, weight):
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
            return f"{self} has latitude {self.lat:.2f}, longitude {self.long:.2f} , is full, and has weight {self.weight:.2f} kg " 
        else:
            return f"{self} has latitude {self.lat:.2f}, longitude {self.long:.2f} , is not full, and has weight {self.weight:.2f} kg " 

if __name__ == "__main__":
    bin2 = Bin(3,4,False,5)
    print(str(bin2))
    bin2.update(5,6,True,7)
    print(str(bin2))


