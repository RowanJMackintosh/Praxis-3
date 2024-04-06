import json
from pathlib import Path

import bin

'''
The "database" here is a python list of Bin's

This does not make sense to use this class as instances since there is only one of them, so this uses 
class variables for the internal data and class methods, rather then instance methods
'''

# This needs to contain the path inside the android to the file we are persisting the "database" to
FILENAME = "database.json"
FILEPATH = Path(__file__).with_name(FILENAME)

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


def bin_ll_adjust_reverse(bin_a):
    '''
    Take the fixed decimal version of latitude and longitude we are using in the database and convert it back to the float representation.
    We stuff it back into a Bin just so we can pass it back as a unit to the caller.
    This is called to convert a bin for sending it out the network.
    '''
    latitude, longitude = ll_adjust_reverse(bin_a.lat, bin_a.long)
    bin_ = bin.Bin(bin_a.id, latitude, longitude, bin_a.full, bin_a.weight)

    return bin_


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
    
    # FIX: change this to find the bin that is the closest linear distance to the given lat/log and assume that's the bin
    #       maybe have 
    @classmethod
    def find_and_update_bin(cls, latitude, longitude, full_state, weight):
        '''
        This take a latitude and longitude and uses that to find the apropriate bin in the "database".
        It then updates the data related to that bin.
        '''
        # convert latitude and longitude
        latitude_i, longitude_i = ll_adjust(latitude, longitude)
        
        # find the bin
        # This could be done with a list comprehension filter like this:
        #   bin = [bin for bin in cls.bin_data if latitude_i == bin.latitude and longitude_i < bin.longitude][0]
        # but the expanded for is more obvious
        for bin in cls.bin_data:
            if latitude_i == bin.latitude and longitude_i < bin.longitude:
                break
             
        if not bin:
        # This should not happen. The bin at this location was not found in the database
           print(f"ERROR: bin with latitude and longitude ({latitude}, {longitude} not found!") 

        bin.update(latitude_i, longitude_i, full_state, weight)

        return bin

 
    @classmethod
    def filter_by_latitude_longitude(cls, min_latitude, max_latitude, min_longitude, max_longitude):
        '''
        Filter the database and return entries within the min-max latitude longitude range
        '''
        # convert latitudes and longitudes
        min_latitude_i, min_longitude_i = ll_adjust(min_latitude, min_longitude)
        max_latitude_i, max_longitude_i = ll_adjust(max_latitude, max_longitude)

        # find the bins that lie within the specified latitude and logitude range
        filtered_bins = [bin for bin in cls.bin_data if min_latitude_i < bin.lat and bin.lat < max_latitude_i and min_longitude_i < bin.long and bin.long < max_longitude_i]

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
            json_data = json.load(file)
            for datum in json_data:    
                cls.bin_data.append(bin.Bin(**datum))
