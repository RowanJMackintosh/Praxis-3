import datetime

class Full_record:
    def __init__(self, time, weight):
        self.time = time # Time in datetime format when the weight update occured
        self.weight = weight

    
class Bin:
    def __init__(self, id, lat, long, full, weight):
        self.id = id # int representing the id of the bin - if moved to a database model this would correspond to the primary key column in the bin database
        self.lat = lat # float latitude of bin
        self.long = long # float longitude of bin 
        self.full = full # boolean for whether bin is full - True means it's full
        self.weight = weight # int for the current weight of the bin in grams
        self.full_rec_list = [] # this is going to be an array of full_record() entries appended to as weight updates come in (this is for later data mining)


    def get_location(self): # returns location
        return self.lat, self.long


    def get_weight(self): 
        return self.weight


    def update(self, latitude, longitude, fullState, weight):
        # latitude and longitude will be fixed for a bin, why are we updating them
        # self.lat = latitude
        # self.long = longitude

        self.full = fullState
        self.weight = weight

        # need to create a full_rec and append it to full_rec_list
        self.full_rec_list.append(Full_record(datetime.datetime.now(), self.weight))


    def __str__(self):
        if self.full == True:
            return f"{self.id} has latitude {self.lat:.5f}, longitude {self.long:.5f}, is full, and has weight {self.weight:.2f} kg" 
        else:
            return f"{self.id} has latitude {self.lat:.5f}, longitude {self.long:.5f} , is not full, and has weight {self.weight:.2f} kg " 
