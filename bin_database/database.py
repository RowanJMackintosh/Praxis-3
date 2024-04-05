import json

import bin
import map

'''
The "database" here is a python list of Bin's

This does not make sense to use this class as instances since there is only one of them, so this uses 
class variables for the internal data and class methods, rather then instance methods
'''

FILEPATH = "???" # This needs to contain the path inside the android to the file we are persisting the "database" to,

# This is to take the float representation of the latitude and longitude and map it to the fixed decimal version we are using in the database
LL_DIGITS = 10 ** 5

def ll_adjust(latitude, longitude):
        '''
         Take the float representation of the latitude and longitude and map it to the fixed decimal version we are using in the database
         '''
        latitude_i = int(latitude * LL_DIGITS)
        longitude_i = int(longitude * LL_DIGITS)
        return (latitude_i, longitude_i)

def ll_adjust_reverse(latitude_i, longitude_i):
        '''
         Take the fixed decimal version of latitude and longitude we are using in the database and convert it back to the float representation
         '''
        latitude = latitude_i / LL_DIGITS
        longitude = longitude_i / LL_DIGITS
        return (latitude, longitude)


class Database:
    bin_data = []               # This is the list of all bins
    next_id = 0                 # Next available bin id

    # This  @classmethod decorator tells python this is a class method NOT an instance method. This is important!
    # It also means that you use "cls" instead of "self" to refer to the internal class varables (like bin_data)
    @classmethod
    def add_bin(cls, latitude, longitude):
        id = cls.next_id
        cls.next_id += 1
        
        # convert latitude and longitude
        latitude_i, longitude_i = ll_adjust(latitude, longitude)

        cls.bin_data.append(bin.Bin(id, latitude_i, longitude_i, False, 0))

    '''
    I (Rowan) wrote the filter_by_latitude_longitude method already because it is the one I need to get the data for the mapping part of the app.
    Also wrote the update() to demonstrate finding the bin (using the adjusted longitude and latitude) in the list and then calling it's bin.update().
    I also wrote the save and load methods to help out with the json aspect of the program, but someone else needs to figure out what goes in FILEPATH above.

    
    Others will need to add whateve other class methods are needed to access/filter/operate on the bins in the bin_data list
    I expect others to add/write more class methods to fill in the rest of what is needed to access/filter/operate on the bins "database"
    '''
    
    @classmethod
    def find_and_update_bin(cls, latitude, longitude, full_state, weight):
        '''
        This take a latitude and longitude and uses that to find the apropriate bin in the "database".
        It then updates the data related to that bin.
        '''
        # convert latitude and longitude
        latitude_i, longitude_i = ll_adjust(latitude, longitude)
        error = 0.1 #this is to see how much variance we want from the recorded latitude and longitude values for the bin. This can be changed depending on how much
        #variance we typically expect to see in the latitude and longitude values
        
        # find the bin

        filtered = cls.filter_by_latitude_longitude(cls,latitude-error,latitude+error,longitude-error,longitude+error)
        min_e_lat = 10000000 #this is to keep track of the minimum difference from the given latitude - we use a very large number to make sure that the actual min replaces this on the first call
        max_e_long = 10000000 #this is to keep track of the min difference from the given longitude
        ideal_index = 0 #this gives the index of the bin in filtered that is closest to the given lat and long
        i=0 #this keeps track of which bin we are currently on in  filtered
        #this function finds which bin in the filtered list is closest to the given latitude and longitude
        for bin in filtered:
            e_lat = abs(latitude_i -bin.latitude)
            e_long = abs(longitude_i - bin.longitude)
            if e_lat < min_e_lat and e_long < min_e_long:
                min_e_lat = e_lat
                min_e_long = e_long
                ideal_index = i
            i += 1

        #this function finds the bin in the bin database that is closest (linearly) to the given latitude and longitude and then updates the info related to the bin
        ideal_bin_id = filtered[i].id
        for bin in cls.bin_data:
             if ideal_bin_id == bin.id:
                bin.full = full_state
                bin.weight = weight
                break
  
        if not bin:
        # This should not happen. The bin at this location was not found in the database
           print(f"ERROR: bin with latitude and longitude ({latitude}, {longitude} not found!") 

        bin.update(latitude_i, longitude_i, full_state, weight)

    

 
    @classmethod
    def filter_by_latitude_longitude(cls, min_latitude, max_latitude, min_longitude, max_longitude):
        '''
        Filter the database and return entries within the min-max latitude longitude range
        '''
        # convert latitudes and longitudes
        min_latitude_i, min_longitude_i = ll_adjust(min_latitude, min_longitude)
        max_latitude_i, max_longitude_i = ll_adjust(max_latitude, max_longitude)

        # find the bins that lie within the specified latitude and logitude range
        filtered_bins = [bin for bin in cls.bin_data if min_latitude_i < bin.latitude < max_latitude_i and min_longitude_i < bin.longitude < max_longitude_i]

        return filtered_bins
        

    @classmethod
    def save(cls):
        '''
        A method to save/persist the bin_data out to a file
        '''
        with open(FILEPATH, "w") as file:
            json.dump(cls.bin_data, file)


    @classmethod
    def load(cls):
        '''
        A method to load in the persisted bin_data from a file
        '''
        with open(FILEPATH, "r") as file:
            cls.bin_data = json.load(file)