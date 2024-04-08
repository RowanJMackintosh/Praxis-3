
import os
import threading
from pathlib import Path


MAX_WEIGHT = 90

# FIX - This is for testing, Where is the real path?

FILENAME = "example_readings.txt"
BIN_UPDATE_FILE_PATH = Path(__file__).with_name(FILENAME)


class Update:
    def __init__(self, lat, long, full, weight):
        self.lat = lat # float latitude of bin
        self.long = long # float longitude of bin 
        self.full = full # boolean for whether bin is full - True means it's full
        self.weight = weight # int for the current weight of the bin in grams

    def __str__(self):
        if self.full == True:
            return f"latitude {self.lat:.5f}, longitude {self.long:.5f}, is full, and has weight {self.weight:.2f} kg" 
        else:
            return f"latitude {self.lat:.5f}, longitude {self.long:.5f} , is not full, and has weight {self.weight:.2f} kg " 


def full_status(weight):
    if weight >= 0.7 * MAX_WEIGHT:
        return True
    return False
    
def get_bin_updates():
    updates = []


    new_file = BIN_UPDATE_FILE_PATH+"_tmp"
    try:
        os.rename(BIN_UPDATE_FILE_PATH, new_file)

        with open(new_file, "r") as file: #fill in the name of the file

            while True:
                temp = []
            
                # Get next line from file
                line = file.readline()
                # if line is empty
                # end of file is reached
                if not line:
                    break

                update = parse_update(line)
                if update:
                    updates.append(update)
    except FileNotFoundError:
        return None
    finally:
        os.remove(new_file)


def parse_update(line):
    
    # A valid line will look like this "57.562,3.859,-1271.0,([0.0, 'N'], [0.0, 'W'])"
    # look for the "(" to break it and also test if it is valid or a header line
    try:
        first, second = line.split('(')
    except ValueError:
        # This is not a line formated with a () in it so it is not a valid line (likely the header) -discard line
        return
        
    try:
        # This first string will look like this "57.562,3.859,-1271.0,"
        US1_s, US2_s, load_s, _ = first.split(",")
        # load_s looks like "-1271.0" and we want an int so we need to convert the string to a float, then an int
        weight = int(float(load_s)/1000)

        # second looks like this "[0.0, 'N'], [0.0, 'W'])" and we need to get signed floats from this. Not N/S E/W.
        _, lat_temp_s, long_temp_s = second.split("[")
        # will now look something like "0.0, 'N'], "
        lat_s, dir = lat_temp_s.split("]")[0].split(", ")
        sign = 1 if dir == "'N'" else -1
        lat = float(lat_s) * sign
        
        long_s, dir = long_temp_s.split("]")[0].split(", ")
        sign = 1 if dir == "'E'" else -1
        long = float(lat_s) * sign

        update = Update(lat, long, full_status(weight), weight)
        #print(f"   update: {update}")
        return update
        
    except ValueError:
        return


'''
class Reader_Server:


    def __init__(self):
        self.server = None


    def start(self):
        self.server = threading.Thread(target=self.reader_server)
        self.server.start()


    def reader_server(self):
        
        time.sleep(10)
        
        client = Client("aragolaa", "aio_LfUu68p7cpa5GuH3rscznuLAFkVj")
        
        data_string = client.receive("information") 
        
        if prev_string != data_string:
            if os.path.exists("data_loader/readings.txt"):
                clear_file = (clear_file + 1)%30
                with open("data_loader/readings.txt", "a+") as file:
                    file.write(data_string.value + " | " + data_string.updated_at + "\n")
        
        if clear_file == 29:
            open("data_loader/readings.txt", 'w').close()
        
'''