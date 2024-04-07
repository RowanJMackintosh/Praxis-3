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


class Database:
    bin_data = []               # This is the list of all bins
    next_id = 0                 # Next available bin id

    # This  @classmethod decorator tells python this is a class method NOT an instance method. This is important!
    # It also means that you use "cls" instead of "self" to refer to the internal class varables (like bin_data)
    @classmethod
    def add_bin(cls, latitude, longitude):
        id = cls.next_id
        cls.next_id += 1

        cls.bin_data.append(bin.Bin(id, latitude, longitude, False, 0))

    '''
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
  
        # find the bin
        # This could be done with a list comprehension filter like this:
        #   bin = [bin for bin in cls.bin_data if latitude == bin.latitude and longitude == bin.longitude][0]
        # but the expanded for is more obvious
        for bin in cls.bin_data:
            if latitude == bin.latitude and longitude == bin.longitude:
                break
             
        if not bin:
        # This should not happen. The bin at this location was not found in the database
           print(f"ERROR: bin with latitude and longitude ({latitude}, {longitude} not found!") 

        bin.update(latitude, longitude, full_state, weight)

        return bin

 
    @classmethod
    def filter_by_latitude_longitude(cls, min_latitude, max_latitude, min_longitude, max_longitude):
        '''
        Filter the database and return entries within the min-max latitude longitude range
        '''

        # find the bins that lie within the specified latitude and logitude range
        filtered_bins = [bin for bin in cls.bin_data if min_latitude < bin.lat < max_latitude and min_longitude < bin.long < max_longitude]

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
